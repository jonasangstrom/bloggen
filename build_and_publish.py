import os
print('starting build script')
os.system('bundle exec jekyll build')
os.system('aws s3 sync public/ s3://www.anion.se --acl public-read --delete')
os.system('aws cloudfront create-invalidation --distribution-id E379E2RCB0S37Y --paths /*')
print('build done')