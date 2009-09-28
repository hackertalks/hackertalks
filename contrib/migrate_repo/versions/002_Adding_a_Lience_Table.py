import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base 

from migrate import *

Base = declarative_base()
Base.metadata.bind = migrate_engine

talks_speakers_table = sa.Table('talks_speakers', Base.metadata,
    sa.Column('talk_id', sa.types.Integer(), sa.ForeignKey('talks.id'), primary_key=True),
    sa.Column('speaker_id', sa.types.Integer(), sa.ForeignKey('speakers.id'), primary_key=True),
    )

class Speaker(Base):
    __tablename__ = 'speakers'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    job_title = sa.Column(sa.types.Unicode())


class License(Base):
    __tablename__ = 'licenses'
    
    id = sa.Column(sa.types.Integer(), primary_key=True)
    name = sa.Column(sa.types.Unicode())
    shortname = sa.Column(sa.types.Unicode())
    abbreviation = sa.Column(sa.types.Unicode())
    link = sa.Column(sa.types.Unicode())
    thumbnail = sa.Column(sa.types.Unicode())
    shareable = sa.Column(sa.types.Boolean())
    description = sa.Column(sa.types.UnicodeText())

class Talk(Base):
    __tablename__ = 'talks'

    id = sa.Column(sa.types.Integer(), primary_key=True)
    short_title = sa.Column(sa.types.Unicode())
    title = sa.Column(sa.types.Unicode())
    description = sa.Column(sa.types.UnicodeText())
    thumbnail_url = sa.Column(sa.types.Unicode())
    recording_date = sa.Column(sa.types.Date())
    video_duration = sa.Column(sa.types.Interval())
    video_embedcode = sa.Column(sa.types.UnicodeText())
    video_bliptv_id = sa.Column(sa.types.Integer())
    license = sa.Column(sa.types.Integer(), sa.ForeignKey('licenses.id'))
    speakers = orm.relation('Speaker', secondary=talks_speakers_table, backref='talks')
    


def upgrade():
    License.__table__.create()
    conn = migrate_engine.connect()
    conn.execute("ALTER TABLE talks DROP COLUMN license")
    conn.execute("ALTER TABLE talks ADD license INTEGER")
    conn.execute("ALTER TABLE talks ADD CONSTRAINT talks_license_fkey FOREIGN KEY(license) REFERENCES licenses (id)")
    Session = Session = orm.scoped_session(orm.sessionmaker())
    Session.configure(bind=migrate_engine)
    
    Session.add(License(name=u'No license (All rights reserved)', shortname=u'All rights reserved', abbreviation=u'(C)', link=u'', thumbnail=u'', shareable=False, description=u'<p>By not selecting a license you retain all rights to your media granted by law.</p><p>You may want to consider choosing a Creative Commons license to allow more liberal use and sharing of your media, though. There are lots of good reasons to choose a Creative Commons license &#151; not the least of which is that doing so helps enrich the world we live in. Check out <a href=\"http://creativecommons.org/\" target=\"_BLANK\">CreativeCommons.org</a> for more information.</p>'))
    Session.add(License(name=u'Creative Commons Attribution 2.0', shortname=u'Attribution', abbreviation=u'by/2.0', link=u'http://creativecommons.org/licenses/by/2.0/', thumbnail=u'http://i.creativecommons.org/l/by/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NoDerivs 2.0', shortname=u'Attribution-NoDerivs', abbreviation=u'by-nd/2.0', link=u'http://creativecommons.org/licenses/by-nd/2.0/', thumbnail=u'http://i.creativecommons.org/l/by-nd/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial-NoDerivs 2.0', shortname=u'Attribution-NonCommercial-NoDerivs', abbreviation=u'by-nc-nd/2.0', link=u'http://creativecommons.org/licenses/by-nc-nd/2.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc-nd/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use the work for commercial purposes.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial 2.0', shortname=u'Attribution-NonCommercial', abbreviation=u'bc-nc/2.0', link=u'http://creativecommons.org/licenses/by-nc/2.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial-ShareAlike 2.0', shortname=u'Attribution-ShareAlike', abbreviation=u'by-nc-sa/2.0', link=u'http://creativecommons.org/licenses/by-nc-sa/2.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc-sa/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-ShareAlike 2.0', shortname=u'Public Domain', abbreviation=u'by-sa/2.0', link=u'http://creativecommons.org/licenses/by-sa/2.0/', thumbnail=u'http://i.creativecommons.org/l/by-sa/2.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of this work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Public Domain', shortname=u'', abbreviation=u'pd', link=u'http://creativecommons.org/licenses/publicdomain/', thumbnail=u'http://mirrors.creativecommons.org/presskit/icons/pd.png', shareable=True, description=u'<p>By placing a work in the public domain you are disclaiming all copyright to the work for the benefit of the public at large.</p><p>Once placed in the public domain, the Work may be freely reproduced, distributed, transmitted, used, modified, built upon, or otherwise exploited by anyone for any purpose, commercial or non-commercial, and in any way, including by methods that have not yet been invented or conceived.</p>'))
    Session.add(License(name=u'Creative Commons Attribution 3.0', shortname=u'Attribution', abbreviation=u'by/3.0', link=u'', thumbnail=u'http://i.creativecommons.org/l/by/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NoDerivs 3.0', shortname=u'Attribution-NoDerivs', abbreviation=u'by-nd/3.0', link=u'http://creativecommons.org/licenses/by-nd/3.0/', thumbnail=u'http://i.creativecommons.org/l/by-nd/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial-NoDerivs 3.0', shortname=u'Attribution-NonCommercial-NoDerivs', abbreviation=u'by-nc-nd/3.0', link=u'http://creativecommons.org/licenses/by-nc-nd/3.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use the work for commercial purposes.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial 3.0', shortname=u'Attribution-NonCommercial', abbreviation=u'by-nc/3.0', link=u'http://creativecommons.org/licenses/by-nc/3.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-NonCommercial-ShareAlike 3.0', shortname=u'Attribution-ShareAlike', abbreviation=u'by-nc-sa/3.0', link=u'http://creativecommons.org/licenses/by-nc-sa/3.0/', thumbnail=u'http://i.creativecommons.org/l/by-nc=sa/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'))
    Session.add(License(name=u'Creative Commons Attribution-ShareAlike 3.0', shortname=u'Public Domain', abbreviation=u'by-nd/3.0', link=u'http://creativecommons.org/licenses/by-sa/3.0/', thumbnail=u'http://i.creativecommons.org/l/by-nd/3.0/88x31.png', shareable=True, description=u'<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of this work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'))
    Session.commit()

def downgrade():
    conn = migrate_engine.connect()
    conn.execute("ALTER TABLE talks DROP CONSTRAINT talks_license_fkey")
    conn.execute("ALTER TABLE talks DROP COLUMN license")
    conn.execute("ALTER TABLE talks ADD license TEXT")
    License.__table__.drop()
