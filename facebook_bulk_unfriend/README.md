# Facebook Bulk Unfriend Helper

This tool helps you:
1. Load your Facebook friends list page.
2. Auto-select likely inactive (older than N months) and/or deactivated accounts.
3. Auto-select duplicate-name accounts (keeps one, selects the rest).
4. Select friends in bulk.
5. Unselect people you want to keep.
6. Unfriend only the selected people.

## Important
- Use at your own risk and follow Facebook's Terms of Service.
- Facebook UI changes can break automation selectors over time.
- Start with a small batch first (for example, 5 people).

## Setup
1. Install the Tampermonkey extension in your browser.
2. Create a new Tampermonkey script.
3. Paste in the contents of `facebook_bulk_unfriend.user.js`.
4. Save the script.

## Use
1. Go to your friends page (example: `https://www.facebook.com/me/friends`).
2. Wait for the "FB Bulk Unfriend" panel to appear on the right.
3. Click `Scan Visible` (or `Auto Scroll + Scan` to load more).
4. For auto-filtering: choose rules (`Inactive`, months, `Deactivated`) and click `Find & Select Targets`.
5. Keep `Hidden=>Inactive` enabled to treat profiles with hidden activity as inactive candidates.
6. If needed, also enable `Unknown` and run `Find & Select Targets` again.
7. Click `Select Duplicate Names` to select duplicate-name accounts (it keeps one account from each same-name group).
8. (Optional) Click `Select All` if you want manual bulk selection instead.
9. Uncheck people you want to keep manually, or paste names (one per line) in `Keep Names` and click `Unselect Keep Names`.
10. Click `Unfriend Selected`.

## Tips
- Keep names are matched case-insensitively.
- Inactive detection is heuristic (best-effort based on profile data Facebook exposes). Facebook can hide this data, resulting in `Unknown` profiles.
- Duplicate selection groups by exact same visible name text and keeps the first loaded card from each duplicate group.
- If Facebook asks for extra confirmations, complete them manually and continue.
- Use `Stop` if you need to pause mid-run.

