from datetime import datetime
from bson import ObjectId

class Job:
    def __init__(self, title, company, location, description, link, platform, date_posted=None):
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.link = link
        self.platform = platform
        self.date_posted = date_posted or datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "link": self.link,
            "platform": self.platform,
            "date_posted": self.date_posted
        }