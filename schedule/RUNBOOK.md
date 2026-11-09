# 9 November 2026 — channel clean-up and re-upload (runbook)

Agreed with the channel owner on 8 Nov 2026. Runs only on **9 Nov 2026**, at 07:12 (start, moved up by the owner), 08:00, 09:00, 10:00, 11:00 and 12:00 (last)
Europe/Istanbul (UTC+3). Each run is one scheduled message into this session.

Channel: **Somewhere Right Now** — channel id `UCjtP6wFSjGODBeP9fAtX_yQ`, uploads playlist `UUjtP6wFSjGODBeP9fAtX_yQ`.
All YouTube calls go through the Zapier YouTube app (`selected_api: YouTubeV4CLIAPI`, default connection
`021db79f-79eb-857f-a1f6-8b591af2d90f`):
- read: `execute_zapier_read_action`, action `_zap_raw_request`, tool_name `youtube_make_api_get_request`
- delete: `execute_zapier_write_action`, action `_zap_raw_request`, tool_name `youtube_make_api_mutating_request`,
  method `DELETE`, url `https://www.googleapis.com/youtube/v3/videos`, querystring `{"id": "<videoId>"}`
- upload: `execute_zapier_write_action`, action `upload_video`, tool_name `youtube_upload_video`

## Rules (the owner's instructions)

1. **08:00 run:** read every video on the channel (all pages of the uploads playlist, then `videos?part=snippet,statistics`).
   Every video with **fewer than 20 views** is deleted — including videos that are not ours (their files are not here;
   they are deleted for good, as the owner asked).
2. Before deleting a video, save its title, description, tags, categoryId, publishedAt and viewCount in `state.json`.
3. Our videos are the files in `mine/<videoId>.mp4`. Each of ours that was deleted is uploaded again, **public**, with the
   title, description, tags and category_id from `schedule/metadata.json` (keyed by the OLD videoId; written for reach,
   the owner handed titles, descriptions and tags to us), `made_for_kids: false`, `notify_subscribers: false`,
   video URL `https://raw.githubusercontent.com/SomewhRightNow/videos/main/mine/<videoId>.mp4`.
   **The owner said no confirmation is needed on the morning: run every step without asking.**
4. Re-uploads are spread over the runs from 07:12 to 12:00: each run uploads `ceil(remaining / runs_left)`,
   runs_left counting this run. The 12:00 run uploads everything still queued.
5. **08:00–12:00 runs** scan the channel again and delete videos under 20 views **except** any video published at or after
   07:12 Istanbul on 9 Nov (the start) (publishedAt >= `2026-11-09T04:12:47Z`) — that protects the morning's re-uploads and anything
   the owner posts from the start on. Any of ours deleted in a later scan joins the upload queue.
6. Never delete a video published on or after `2026-11-09T04:12:47Z`. Videos published overnight before 08:00 (e.g.
   TjJYBN6bBAw, 02:15 Istanbul) were scanned like the rest in the first run. Never upload a file that is not in `mine/`.
7. After each run: write `state.json`, commit and push it, and post a short report in the chat (deleted, uploaded with new
   links, queue left). After the 12:00 run, give the final summary.

## If the machine was restarted

The clone lives at `/home/user/videos`. If it is missing:
`git clone --depth 1 https://github.com/SomewhRightNow/videos /home/user/videos` (the repo is attached to the session).
Before writing state: `git -C /home/user/videos pull --ff-only`.
