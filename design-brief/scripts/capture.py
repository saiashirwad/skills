#!/usr/bin/env python3
"""Capture full pages; original local mechanics, not vendored third-party code."""
import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
from urllib.request import urlopen


def arguments():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Requires Playwright and its Chromium in the selected Python environment. "
        "Example: python3 capture.py --url A=http://127.0.0.1:4321/?variant=A "
        "--url B=http://127.0.0.1:4321/?variant=B --command 'npm run dev' "
        "--ready '[data-ready]' --out /path/to/captures. "
        "Outputs PNGs, manifest.json, and server.log (when starting a server)."
    ))
    parser.add_argument('--url', action='append', required=True, metavar='KEY=URL')
    parser.add_argument('--command', help='Optional trusted server command, run in --cwd.')
    parser.add_argument('--cwd', default='.')
    parser.add_argument('--out', required=True)
    parser.add_argument('--ready', default='body', help='Visible readiness selector; use an app-specific marker for async pages.')
    parser.add_argument('--timeout', type=float, default=30, help='Per-check timeout in seconds.')
    args = parser.parse_args()
    args.urls = []
    for item in args.url:
        key, separator, url = item.partition('=')
        if not separator or not re.fullmatch(r'[A-Za-z0-9_-]+', key) or not url.startswith(('http://', 'https://')):
            parser.error('--url must be a safe unique KEY=http(s)://URL')
        if key in dict(args.urls):
            parser.error('variant keys must be unique')
        args.urls.append((key, url))
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    return args


def wait_server(url, server, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if server.poll() is not None:
            raise RuntimeError('Server exited before readiness; see server.log')
        try:
            with urlopen(url, timeout=min(1, timeout)) as response:
                if response.status < 400:
                    return
        except Exception:
            time.sleep(0.1)
    raise TimeoutError(f'Server readiness timed out: {url}')


def ready(page, selector):
    page.locator(selector).first.wait_for(state='visible')
    page.wait_for_function('document.fonts.status === "loaded"')
    # Scroll to trigger lazy images without using networkidle on streaming pages.
    for _ in range(100):
        at_bottom = page.evaluate('''() => {
            window.scrollBy(0, window.innerHeight);
            return window.scrollY + window.innerHeight >= document.documentElement.scrollHeight;
        }''')
        page.wait_for_timeout(50)
        if at_bottom:
            break
    else:
        raise RuntimeError('Page did not end within 100 scrolls')
    page.wait_for_function('Array.from(document.images).every(i => i.complete)')
    broken = page.evaluate('Array.from(document.images).filter(i => !i.naturalWidth).map(i => i.currentSrc || i.src)')
    if broken:
        raise RuntimeError(f'Broken images: {broken}')
    page.evaluate('window.scrollTo(0, 0)')


def main():
    args = arguments()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit('Missing Playwright. Use the project environment or install it in an isolated environment, then run python -m playwright install chromium.')
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'captures': [], 'errors': [], 'note': 'Inspect images and test keyboard/motion behavior; capture success is not a visual or accessibility pass.'}
    server = log = None
    try:
        if args.command:
            log = (out / 'server.log').open('w')
            server = subprocess.Popen(args.command, shell=True, cwd=args.cwd, stdout=log,
                                      stderr=subprocess.STDOUT, start_new_session=True)
            wait_server(args.urls[0][1], server, args.timeout)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                for key, url in args.urls:
                    for device, viewport in [('desktop', {'width': 1440, 'height': 1000}),
                                             ('phone', {'width': 390, 'height': 844})]:
                        for theme in ('light', 'dark'):
                            for motion in ('no-preference', 'reduce'):
                                name = f'{key}-{device}-{theme}-{motion}.png'
                                record = {'variant': key, 'url': url, 'viewport': viewport,
                                          'theme': theme, 'motion': motion, 'path': name, 'errors': []}
                                context = browser.new_context(viewport=viewport, color_scheme=theme,
                                                              reduced_motion=motion)
                                try:
                                    page = context.new_page()
                                    page.set_default_timeout(args.timeout * 1000)
                                    page.on('pageerror', lambda error: record['errors'].append(str(error)))
                                    page.on('console', lambda message: record['errors'].append(message.text)
                                            if message.type == 'error' else None)
                                    response = page.goto(url, wait_until='domcontentloaded')
                                    if response is None or response.status >= 400:
                                        raise RuntimeError(f'Navigation failed: {response.status if response else "no response"}')
                                    ready(page, args.ready)
                                    page.screenshot(path=str(out / name), full_page=True)
                                    record['captured'] = True
                                except Exception as error:
                                    record['errors'].append(str(error))
                                    record['captured'] = False
                                finally:
                                    context.close()
                                    manifest['captures'].append(record)
            finally:
                browser.close()
    except Exception as error:
        manifest['errors'].append(str(error))
    finally:
        if server:
            # Kill the whole owned process group, including task-runner children.
            try:
                os.killpg(server.pid, signal.SIGTERM)
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(server.pid, signal.SIGKILL)
                server.wait()
            except ProcessLookupError:
                pass
        if log:
            log.close()
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    failed = bool(manifest['errors'] or any(item['errors'] for item in manifest['captures']))
    print(out / 'manifest.json')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
