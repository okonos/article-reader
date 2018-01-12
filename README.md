# Notice
For the newspaper module to work on AWS Lambda, it's necessary to modify its settings.py file,
as specified in [this PR](https://github.com/codelucas/newspaper/pull/354) (unless already merged), so that it uses temp dir instead of home dir for settings.

Besides, bucket name has to be given both in 
[reader.py](https://github.com/Okonos/article-reader/blob/5dabcc35663d02d17f6d56270b0f32962aaaa54b/reader.py#L8) and 
[zappa_settings.yml](https://github.com/Okonos/article-reader/blob/5dabcc35663d02d17f6d56270b0f32962aaaa54b/zappa_settings.yml#L2).
