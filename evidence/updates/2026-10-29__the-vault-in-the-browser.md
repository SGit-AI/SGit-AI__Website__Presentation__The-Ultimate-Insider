# 29 October 2026, 08:20 UTC: the evidence vault in the browser

The browser link does open the vault: in a headless browser it showed the folder tree and the README after 2 minutes 48 seconds, read only, with no console error and no failed request. It is slow, not broken.

Why: of 615 requests, 395 read the vault's tree and commit objects, one request each, one after another (642 KB in all). The raw captures are not fetched until a file is opened: the whole visit moved 3.4 MB. The time goes on the number of folders (one per source, 382 of them), not on their size. The team's board, with a few dozen folders, opens in seconds.

What would make it fast: fewer folders in the vault people browse. If the editor chooses to rotate the vault (D12), the new one can hold the register only (README, METHOD, BEFORE-TONIGHT, claims, ideas, incidents, studio, proposals, updates and the manifest), with the raw captures in a second vault that is cloned, not browsed. Until then, the clone command in the site's evidence-vault.json is the quick way in.
