# J. Jacobs & Associates — Favicon / App-Icon Kit

The JJA diamond emblem (cropped from `assets/img/logo.jpeg`), packaged for reuse across
every JJA web app/project. Navy diamond + gray waves on a white rounded square.

## Files
| File | Use |
|---|---|
| `favicon.svg` | Modern browser tab icon (scalable, ~16 KB) |
| `favicon.ico` | Legacy/fallback tab icon (16/32/48 multi-size) |
| `apple-touch-icon.png` | iOS/iPadOS home-screen icon (180×180) |
| `favicon-16.png`, `favicon-32.png`, `favicon-48.png` | Explicit PNG sizes |
| `icon-192.png`, `icon-512.png` | PWA / Android / manifest |
| `site.webmanifest` | Optional PWA manifest |

## How to add it to another project
1. Copy the kit files into that project's **public root** (where its HTML is served).
2. Put this in the `<head>` of each page (or the shared template/layout):

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Browsers auto-discover `/favicon.ico` and `/apple-touch-icon.png` at the site root even
without `<link>` tags, so at minimum just dropping those two files in the root works.

3. Bump any cache-bust string if the app uses one — favicons are cached hard; a tab may
   show the old icon until a hard refresh (Ctrl+Shift+R) or browser restart.

## Source
Regenerate from the master logo any time; emblem is auto-cropped from `assets/img/logo.jpeg`.
