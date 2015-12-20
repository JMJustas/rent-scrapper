try:
	import cPickle as pickle
except:
	import pickle
import smtplib, json, os, random, time
import scrappers 

class MailSender:
    def __init__(self, config):
        self.to = config['email']['to']
        self.config = config['email']['smtp']

    def notify(self, records):
        msg = ''
        for record in records:
            msg += 'Price: %6.2f  |  url: %s\n' % (record['price'], record['url'])

        print "Sending mail..."
        smtpserver = smtplib.SMTP(self.config['server'], self.config['port'])
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        sender = self.config['login'] 
        password = self.config['password']
        smtpserver.login(sender, password)

        header = 'To:' + self.to + '\n' + 'From: ' + sender + '\n' + 'Subject: New articles found!\n'
        msg = header + '\n' + msg
        print msg
        smtpserver.sendmail(sender, self.to, msg)
        print "Mail notification sent!"

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, 'config.json')
    data_file = os.path.join(current_dir, 'data.obj')
    config = {}
    with open(config_file, 'rb') as handle:
        config = json.load(handle)

    # sleep for up to sleep_time_max seconds to randomize script run time
    if config['sleep_time_max'] > 0:
        sleep_time = random.randint(0, config['sleep_time_max'])
        print 'sleeping for %d seconds before executing...' % sleep_time 
        time.sleep(sleep_time) 
    print "Starting..."
    
    SCRAPPERS = [
                scrappers.AruodasScrapper(config)
            ]
    data = {}
    # Load previously stored data - we want to remember which articles we've already seen
    try:
        with open(data_file, 'rb') as handle:
            data = pickle.load(handle)
    except:
        pass

    # let's see if we have something new to see
    new_records = []
    for scrapper in SCRAPPERS:
        new_records += [entry for entry in  scrapper.scrape() if entry['url'] not in data]

    # sort by price ASC
    new_records.sort(key=lambda x: x['price'])

    # notify user about new records found
    if len(new_records) > 0:
        MailSender(config).notify(new_records)

        # store records for future reference
        for entry in new_records:
                data[entry['url']] = entry
        with open(data_file, 'wb') as handle:
                pickle.dump(data, handle)
    else:
        print 'No new records found.'

