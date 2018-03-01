from cerebralcortex.core.data_manager.raw.stream_handler import DataSet
from cerebralcortex.cerebralcortex import CerebralCortex
from cerebralcortex.core.datatypes.datastream import DataStream
from cerebralcortex.core.datatypes.datastream import DataPoint
from computefeature import ComputeFeatureBase
from save_feature_stream import store_data

import datetime
import numpy as np
from datetime import timedelta


feature_class_name='PhoneFeatures'



class PhoneFeatures(ComputeFeatureBase):


    def inter_event_time_list(self, data):
        if len(data)==0:
            return None

        last_end = data[0].end_time

        ret = []
        flag = False
        for cd in data:
            if flag == False:
                flag = True
                continue
            dif = cd.start_time - last_end
            ret.append(max(0, dif.total_seconds()))
            last_end = max(last_end, cd.end_time)

        return list(map(lambda x: x/60.0, ret))


    def average_inter_phone_call_sms_time_hourly(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)

        new_data = []
        for h in range(0, 24):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data


    def average_inter_phone_call_sms_time_four_hourly(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)

        new_data = []
        for h in range(0, 24, 4):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(hours=3, minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data



    def average_inter_phone_call_sms_time_daily(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)
        start_time = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day)
        end_time = start_time + datetime.timedelta(hours=23, minutes=59)
        new_data = [DataPoint(start_time=start_time, end_time=end_time, offset=combined_data[0].offset, sample= sum(self.inter_event_time_list(combined_data)) / (len(combined_data)-1))]

        return new_data


    def variance_inter_phone_call_sms_time_daily(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)
        start_time = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day)
        end_time = start_time + datetime.timedelta(hours=23, minutes=59)

        new_data = [DataPoint(start_time=start_time, end_time=end_time, offset=combined_data[0].offset, sample= np.var(self.inter_event_time_list(combined_data)) )]

        return new_data


    def variance_inter_phone_call_sms_time_hourly(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)

        new_data = []
        for h in range(0, 24):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=np.var(self.inter_event_time_list(datalist))))

        return new_data


    def variance_inter_phone_call_sms_time_four_hourly(self, phonedatastream: DataStream, smsdatastream: DataStream):

        if len(phonedatastream.data)+len(smsdatastream.data) <=1:
            return None

        tmpphonestream = phonedatastream
        tmpsmsstream = smsdatastream
        for s in tmpphonestream.data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)
        for s in tmpsmsstream.data:
            s.end_time = s.start_time

        combined_data = phonedatastream.data + smsdatastream.data

        combined_data.sort(key=lambda x:x.start_time)

        new_data = []
        for h in range(0, 24, 4):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(hours=3, minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=np.var(self.inter_event_time_list(datalist))))

        return new_data



    def average_inter_phone_call_time_hourly(self, phonedatastream: DataStream):

        if len(phonedatastream.data) <=1:
            return None

        combined_data = phonedatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)

        new_data = []
        for h in range(0, 24):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data


    def average_inter_phone_call_time_four_hourly(self, phonedatastream: DataStream):

        if len(phonedatastream.data) <=1:
            return None

        combined_data = phonedatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)


        new_data = []
        for h in range(0, 24, 4):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(hours=3, minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data


    def average_inter_phone_call_time_daily(self, phonedatastream: DataStream):

        if len(phonedatastream.data) <=1:
            return None

        combined_data = phonedatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)

        start_time = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day)
        end_time = start_time + datetime.timedelta(hours=23, minutes=59)
        new_data = [DataPoint(start_time=start_time, end_time=end_time, offset=combined_data[0].offset, sample= sum(self.inter_event_time_list(combined_data)) / (len(combined_data)-1))]

        return new_data



    def average_inter_sms_time_hourly(self, smsdatastream: DataStream):

        if len(smsdatastream.data) <=1:
            return None

        combined_data = smsdatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)

        new_data = []
        for h in range(0, 24):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data


    def average_inter_sms_time_four_hourly(self, smsdatastream: DataStream):

        if len(smsdatastream.data) <=1:
            return None

        combined_data = smsdatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)


        new_data = []
        for h in range(0, 24, 4):
            datalist = []
            start = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day, hour=h)
            end = start + datetime.timedelta(hours=3, minutes=59)
            for d in combined_data:
                if start<=d.start_time<=end or start<=d.end_time<=end:
                    datalist.append(d)
            if len(datalist) <=1:
                continue
            new_data.append(DataPoint(start_time=start, end_time=end, offset=combined_data[0].offset, sample=sum(self.inter_event_time_list(datalist))/(len(datalist)-1)))

        return new_data


    def average_inter_sms_time_daily(self, smsdatastream: DataStream):

        if len(smsdatastream.data) <=1:
            return None

        combined_data = smsdatastream.data

        for s in combined_data:
            s.end_time = s.start_time + datetime.timedelta(seconds=s.sample)

        start_time = datetime.datetime(year=combined_data[0].start_time.year, month=combined_data[0].start_time.month, day=combined_data[0].start_time.day)
        end_time = start_time + datetime.timedelta(hours=23, minutes=59)
        new_data = [DataPoint(start_time=start_time, end_time=end_time, offset=combined_data[0].offset, sample= sum(self.inter_event_time_list(combined_data)) / (len(combined_data)-1))]

        return new_data


    def all_users_data(self, study_name: str):

        all_users = self.CC.get_all_users(study_name)

        if all_users:
            for user in all_users:
                streams = self.CC.get_user_streams(user["identifier"])
                self.process_data(user["identifier"], streams)
        else:
            print(study_name, "- study has 0 users.")

    #['CU_CALL_DURATION--edu.dartmouth.eureka', 'CU_SMS_LENGTH--edu.dartmouth.eureka']

    def process_day_data(self, user_id, callstream, smsstream, input_stream1, input_stream2):
        try:
            data = self.average_inter_phone_call_sms_time_hourly(callstream, smsstream)
            if data:
                store_data("metadata/average_inter_phone_call_sms_time_hourly.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:", str(e))
            
        try:
            data = self.average_inter_phone_call_sms_time_four_hourly(callstream, smsstream)
            if data:
                store_data("metadata/average_inter_phone_call_sms_time_four_hourly.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_phone_call_sms_time_daily(callstream, smsstream)
            if data:
                store_data("metadata/average_inter_phone_call_sms_time_daily.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.variance_inter_phone_call_sms_time_daily(callstream, smsstream)
            if data:
                store_data("metadata/variance_inter_phone_call_sms_time_daily.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.variance_inter_phone_call_sms_time_hourly(callstream, smsstream)
            if data:
                store_data("metadata/variance_inter_phone_call_sms_time_hourly.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.variance_inter_phone_call_sms_time_four_hourly(callstream, smsstream)
            if data:
                store_data("metadata/variance_inter_phone_call_sms_time_four_hourly.json", [input_stream1, input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_phone_call_time_hourly(callstream)
            if data:
                store_data("metadata/average_inter_phone_call_time_hourly.json", [input_stream1], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_phone_call_time_four_hourly(callstream)
            if data:
                store_data("metadata/average_inter_phone_call_time_four_hourly.json", [input_stream1], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_phone_call_time_daily(callstream)
            if data:
                store_data("metadata/average_inter_phone_call_time_daily.json", [input_stream1], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_sms_time_hourly(smsstream)
            if data:
                store_data("metadata/average_inter_sms_time_hourly.json", [input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_sms_time_four_hourly(smsstream)
            if data:
                store_data("metadata/average_inter_sms_time_four_hourly.json", [input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        try:
            data = self.average_inter_sms_time_daily(smsstream)
            if data:
                store_data("metadata/average_inter_sms_time_daily.json", [input_stream2], user_id, data, self)
        except Exception as e:
            print("Exception:",str(e))

        
        
    def process_data(self, user_id, stream_names):

        input_stream1 = {}
        input_stream2 = {}
        call_stream_name = 'CU_CALL_DURATION--edu.dartmouth.eureka'
        sms_stream_name = 'CU_SMS_LENGTH--edu.dartmouth.eureka' 
        streams = stream_names
        days = None
        callstream_end_days = None
        smsstream_end_days = None
        for stream_name,stream_metadata in streams.items():
            if stream_name==call_stream_name:
                input_stream1["id"] = stream_metadata["identifier"]
                input_stream1["name"] = stream_metadata["name"]
                callstream_end_days = self.CC.get_stream_duration(input_stream1["id"])
            elif stream_name== sms_stream_name:
                input_stream2["id"] = stream_metadata["identifier"]
                input_stream2["name"] = stream_metadata["name"]
                smsstream_end_days = self.CC.get_stream_duration(input_stream2["id"])
        
        startdate = None
        enddate = None
        
        if callstream_end_days:
            if callstream_end_days["start_time"]:
                startdate = callstream_end_days["start_time"]
            if callstream_end_days["end_time"]:
                enddate = callstream_end_days["end_time"]
            
        if smsstream_end_days:
            if smsstream_end_days['start_time']:
                if startdate and smsstream_end_days['start_time'] < startdate:
                    startdate = smsstream_end_days['start_time']
                else:
                    startdate = smsstream_end_days['start_time']
            if smsstream_end_days['end_time']:
                if enddate and smsstream_end_days['end_time'] > enddate:
                    enddate = smsstream_end_days['end_time']
                else:
                    enddate = smsstream_end_days['end_time']

        days = enddate - startdate
        print(startdate, enddate, days)


        for day in range(days.days + 2):
            day = (startdate + timedelta(days=day)).strftime('%Y%m%d')
            print("Processing day %s" %(str(day)))
            callstream = self.CC.get_stream(input_stream1["id"], user_id=user_id, day=day)
            smsstream = self.CC.get_stream(input_stream2["id"], user_id=user_id, day=day)
            self.process_day_data(user_id,callstream,smsstream,input_stream1,input_stream2)
            

    def process(self):
        if self.CC is not None:
            print("Processing PhoneFeatures")
            self.all_users_data("mperf")
        
    
'''
if __name__ == '__main__':
    # create and load CerebralCortex object and configs
    parser = argparse.ArgumentParser(description='CerebralCortex Reporting Application.')
    parser.add_argument("-cc", "--cc_config_filepath", help="Configuration file path", required=True)
    args = vars(parser.parse_args())

    CC = CerebralCortex(args["cc_config_filepath"])

    # run for all the participants in a study
'''