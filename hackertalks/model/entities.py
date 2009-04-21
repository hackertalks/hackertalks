from elixir import *

class Talk(Entity):
    using_options(tablename='talks')

    id = Field(Integer, primary_key=True)
    title = Field(Unicode)
    description = Field(UnicodeText)
    video_length = Field(Unicode)
    video_embedcode = Field(Unicode)
    
    language = ManyToOne('Language')
    speakers = ManyToMany('Speaker', tablename='talks_speakers')
    tags = ManyToMany('Tag', tablename='talks_tags')
    
    def __repr__(self):
        return "<Talk('%s', '%s', '%s', '%s', '%s')>" % (self.title, self.description, self.language_code, self.video_length, self.video_embedcode)

class Tag(Entity):
    using_options(tablename='tags')
    
    id = Field(Integer, primary_key=True)
    tag = Field(Unicode)
    
    talks = ManyToMany('Talk', tablename='talks_tags')

    def __repr__(self):
        return "<Tag('%s')>" % (self.tag)

class Speaker(Entity):
    using_options(tablename='speakers')
    
    id = Field(Integer, primary_key=True)
    first_name = Field(Unicode)
    last_name = Field(Unicode)
    nickname = Field(Unicode)
    
    talks = ManyToMany('Talk', tablename='talks_speakers')
    
    def __repr__(self):
            return "<Speaker('%s',  '%s', '%s')>" % (self.first_name, self.last_name, self.nickname)

class Language(Entity):
    using_options(tablename='languages')
    
    code = Field(Unicode(3), primary_key=True)
    name = Field(Unicode)
    
    talks = OneToMany('Talk')
    
    def __repr__(self):
        return "<Lanuage('%s', '%s')>" % (self.code, self.name)
    


