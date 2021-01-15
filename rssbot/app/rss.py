from rssreader import RssReader as reader

mr = reader.RssReader('../resources/state.json')

print(mr.get_list())

mr.add_rss_item('cnn', 'http://rss.cnn.com/rss/edition.rss')


