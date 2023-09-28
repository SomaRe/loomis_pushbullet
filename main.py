from pushbullet import Pushbullet
import keys


pb = Pushbullet(keys.PUSHBULLET_ACCESS_TOKEN)
pb.push_note(post.title, post.url)

