" vim: set noexpandtab nolist tabstop=4 shiftwidth=4:
scriptencoding utf-8
if !has('python')
    echo 'fiddle requires python2 support'
    finish
endif

python import fiddle
python fiddle.init()
