# Scheduled uploads of new videos (organised by Claude; the owner handed the channel's organisation to us)

Each scheduled message names one key from `schedule/upcoming.json`. Upload it without asking:
Zapier YouTube `upload_video` (selected_api `YouTubeV4CLIAPI`, tool_name `youtube_upload_video`) with the title,
description, tags and category_id from that entry, `privacy_status: public`, `made_for_kids: false`,
`notify_subscribers: true`, video URL `https://raw.githubusercontent.com/SomewhRightNow/videos/main/upcoming/<key>.mp4`.
Then record the new video id and link in `upcoming.json` (`uploaded_id`), commit, push, and report the link in the chat.
If the clone at /home/user/videos is missing: `git clone --depth 1 https://github.com/SomewhRightNow/videos /home/user/videos`.
