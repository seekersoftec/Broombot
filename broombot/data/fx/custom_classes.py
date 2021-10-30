import os
import multiprocessing
import time
from oandapyV20.contrib.factories import InstrumentsCandlesFactory


class Path(object):
    def __init__(self, path):
        self.path = path
        self.loadPath()

    def loadPath(self):
        import os
        try:
            if os.path.exists(self.path):
                try:
                    FOLDERS = ['/DATASETS']
                    FOLDER_COUNT = 0
                    for folders in FOLDERS:
                        '''If folder is not created or created but deleted..Recreate/Create the folder.
                        Check for all folders in the FOLDERS list'''
                        if not os.path.exists(self.path + FOLDERS[FOLDER_COUNT]):
                            os.makedirs(self.path + FOLDERS[FOLDER_COUNT])
                            print('====== 100% Completed ==== : {}'.format(
                                self.path + FOLDERS[FOLDER_COUNT]))
                            FOLDER_COUNT += 1
                        elif os.path.exists(self.path + FOLDERS[FOLDER_COUNT]):
                            '''OR check if the file is already existing using a boolean..if true return'''
                            print('File Already Existing : {}'.format(
                                self.path + FOLDERS[FOLDER_COUNT]))
                            FOLDER_COUNT += 1
                except OSError as e:
                    '''raise OSError('File Already Existing {}'.format(e))'''
                    print('File Already existing: {}'.format(e))
            elif not os.path.exists(self.path):
                raise OSError(
                    'File self.path: {} does not exist\n\t\tPlease check the self.path again'.format(self.path))
            else:
                print('File Already Existing')
        except Exception as e:
            raise(e)
        finally:
            print('Process completed...Exiting')


class stockDownload(Path):
    def __init__(self, instrument, start, end, client, granular):
        self.instrument = instrument
        self.start = start
        self.end = end
        self.client = client
        self.granular = granular

    def downloadStockData(self):
        '''
          :Arguments:
            :instruments:
              Name of the instrument we are trading
            :start: specify the start date of stcok to download
            :end: specify end date of the stock to download

          :Returntype:
            return the csv file of the downloaded stock in the
            specific folder.
        '''
        def covert_json(reqst, frame):
            for candle in reqst.get('candles'):
                ctime = candle.get('time')[0:19]
                try:
                    rec = '{time},{complete},{o},{h},{l},{c},{v}'.format(time=ctime,
                                                                         complete=candle['complete'],
                                                                         o=candle['mid']['o'],
                                                                         h=candle['mid']['h'],
                                                                         l=candle['mid']['l'],
                                                                         c=candle['mid']['c'],
                                                                         v=candle['volume'])
                except Exception as e:
                    raise(e)
                else:
                    frame.write(rec+'\n')

        # try except to both create folder and enter ticker
        try:
            if not os.path.exists(path + '/DATASETS/{}'.format(self.instrument)):
                os.makedirs(path + '/DATASETS/{}'.format(self.instrument))
            # import the required timeframe
            for timeframe, descrp in self.granular.items():
                with open(path + '/DATASETS/{}/{}_{}.csv'.format(self.instrument, self.instrument, timeframe), 'w') as OUTPUT:
                    params = {'from': self.start,
                              'to': self.end,
                              'granularity': timeframe,
                              'counts': 2500
                              }
                    try:
                        for ii in InstrumentsCandlesFactory(instrument=self.instrument, params=params):
                            print("REQUEST: {} {} {}".format(
                                ii, ii.__class__.__name__, ii.params))
                            self.client.request(ii)
                            covert_json(ii.response, OUTPUT)
                    except:
                        print('{} not available using this API\n Please check your internet connection'.format(
                            instrument))
                    print('********************Done downloading******************\n{}_{}'.format(
                        self.instrument, timeframe))
        except Exception as e:
            raise(e)
        finally:
            print('*'*40)
            print('Stock download completed')
            print('*'*40)


class Run():
    def __init__(self, instrument, timeframe, api, granular, timer, start_fm=None, end_hr=None):
        self.timer = timer
        self.instrument = instrument
        self.timeframe = timeframe
        self.start_fm = start_fm
        self.end_hr = end_hr
        self.api = api
        self.granular = granular
        try:
            if self.timer is None:
                raise ValueError('set timer')
            else:
                if len(self.granular) > 1:
                    thread = []
                    for iterr, granule in enumerate(self.granular):
                        for iterr_time, slp in enumerate(self.timer):
                            if iterr == 0:
                                start = self.timeframe[0][0]
                                end = self.timeframe[0][1]
                                thread.append(multiprocessing.Process(target=self.runMain, args=(
                                    self.granular[iterr], self.timer[iterr], start, end)))
                            elif iterr == 1:
                                start = self.timeframe[1][0]
                                end = self.timeframe[1][1]
                                thread.append(multiprocessing.Process(target=self.runMain, args=(
                                    self.granular[iterr], self.timer[iterr], start, end)))
                    for trd in thread:
                        trd.daemon = True
                        trd.start()
                    for st_trd in thread:
                        st_trd.join()
                else:
                    thread = []
                    for iterr, granule in self.granular:
                        for iterr_time, slp in self.timer:
                            thread.append(multiprocessing.Process(
                                target=self.subMain, args=(granule, slp)))
                    for trd in thread:
                        trd.daemon = True
                        trd.start()
                    for st_trd in thread:
                        st_trd.join()
        except Exception:
            raise ValueError('Thread unable to start')

    def Downloader(self, gran, start, end):
        self.start = start
        self.end = end
        for instr in self.instrument:
            stockDownload(instr, self.start, self.end,
                          self.api, gran).downloadStockData()

    def subDownloader(self, gran):
        for instr in self.instrument:
            stockDownload(instr, self.start_fm, self.end_hr,
                          self.api, gran).downloadStockData()

    def runMain(self, gran, sleeper, start, end):
        self.sleeper = sleeper
        self.start = start
        self.end = end
        begin = time.time()
        while True:
            if not self.instrument:
                break
            elif not self.start:
                break
            elif not self.end:
                break
            elif not self.api:
                raise ValueError('client api not found')
            elif not gran:
                break
            else:
                self.Downloader(gran, self.start, self.end)
            print('finish time %s-secs' % (time.time() - begin))
            print('program running in background')
            time.sleep(self.sleeper)

    def subMain(self, gran, sleeper):
        self.sleeper = sleeper
        begin = time.time()
        while True:
            if not self.instrument:
                break
            elif not self.start:
                break
            elif not self.end:
                break
            elif not self.api:
                raise ValueError('client api not found')
            elif not gran:
                break
            else:
                self.subDownloader(gran)
            print('finish time %s' % (time.time() - begin))
            # print('program running in background')
            # time.sleep(self.sleeper)
