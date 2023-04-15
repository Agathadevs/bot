import yt_dlp
import datetime

def music_info(youtube_url):
    with  yt_dlp.YoutubeDL() as ydl:
        data={}       
        original_data = ydl.extract_info(str(youtube_url), download=False)     
        data["id"] = original_data.get("id")
        data["title"] = original_data.get("title")
        data["thumbnail"] = original_data.get("thumbnail")
        data["uploader"] = original_data.get("uploader")
        data["duration"]= original_data.get("duration") 
        Time_date = original_data.get("duration") 
        minutes,second=divmod(Time_date,60)
        hour,minutes=divmod(minutes,60)
        time=datetime.time(hour,minutes,second)
        
        if hour==0:
            data['Time']=time.strftime("%M:%S")
        else:
            data["Time"]=time.strftime("%H:%M:%S")
        
        data["view_count"] = original_data.get("view_count") 
        data["comment_count"] = original_data.get("comment_count")
        data["like_count"] = original_data.get("like_count")
        data["dislike_count"] = original_data.get("dislike_count")
        data["average_rating"] = original_data.get("average_rating") 
        data["description"] = original_data.get("description") 
        data["tags"] = original_data.get("tags") 
        data["url"] = original_data.get("webpage_url") 
        data["upload_date"] = original_data.get("upload_date")
        data["source"] = original_data.get("source")
    return data 