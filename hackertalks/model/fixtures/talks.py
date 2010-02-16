from fixture import DataSet
from inspect import isclass


class SpeakerData(DataSet):
    class micah:
        name = 'Micah Anderson'
        job_title = None

    class drew:
        name = 'Drew McManus'
        job_title = 'Road 3 Ltd.'

    class bre:
        name = 'Bre Pettis'
        job_title = 'MakerBot'


class TagData(DataSet):
    class security:
        name = 'Security'
    class lol:
        name = 'lol'


class TalkData(DataSet):
    class brestalk:
        short_title = 'Making a RepRap, Part 1'
        title = 'How to build a RepRap for rapid home prototyping (Part 1)'
        description = 'Last year I made this video as an introduction to making your own reprap, a self replicating and rapid prototyping robot.'
        thumbnail_url = 'http://a.images.blip.tv/Oldjewstellingjokes-SyLevineMorrisTheGambler109.jpg'
        recording_date = '2009-06-28'
        video_duration = '00:12:00'
        video_embedcode = '<embed src="http://blip.tv/play/gp0JgZrLeQI" type="application/x-shockwave-flash" width="480" height="300" allowscriptaccess="always" allowfullscreen="true"></embed>'
        video_bliptv_id = 2512747

        speakers = [SpeakerData.bre]
        tags = [TagData.security, TagData.lol]
        slug = 'making_a_reprap_pt1'

    class agilemgmt:
        short_title = 'Agile Management'
        title = 'Agile Management: Advice for Entrepreneurs'
        description = 'Drew McManus of Road 3 shares his advice on managing agile projects. Drew describes when and how much to plan, the right way to share the plan, and how to keep the product and the engineering team properly focused while not losing the grand vision.'
        thumbnail_url = 'http://a.images.blip.tv/Jdollars92-TheFederalAgentEp2Season1240.jpg'
        recording_date = '2009-05-28'
        video_duration = '01:08:00'
        video_embedcode = '<embed src="http://blip.tv/play/gpk2gZueXQI" type="application/x-shockwave-flash" width="480" height="390" allowscriptaccess="always" allowfullscreen="true"></embed>'
        video_bliptv_id = 2523345

        speakers = [SpeakerData.micah, SpeakerData.drew]
        tags = [TagData.security]
        slug = 'agile_mgmt'


class FeaturedTalkData(DataSet):
    class jalol:
        talk = TalkData.brestalk
        date = '2010-01-01'
    class jalolol:
        talk = TalkData.agilemgmt
        date = '2010-01-02'


class LicenseData(DataSet):
    class C:
		name='No license (All rights reserved)'
		shortname='All rights reserved'
		abbreviation = '(C)'
		link = ''
		thumbnail = ''
		description = '<p>By not selecting a license you retain all rights to your media granted by law.</p><p>You may want to consider choosing a Creative Commons license to allow more liberal use and sharing of your media, though. There are lots of good reasons to choose a Creative Commons license &#151; not the least of which is that doing so helps enrich the world we live in. Check out <a href="http://creativecommons.org/" target="_BLANK">CreativeCommons.org</a> for more information.</p>'
		shareable = False
    class by:
		name='Creative Commons Attribution 2.0'
		shortname='Attribution'
		abbreviation = 'by/2.0'
		link = 'http://creativecommons.org/licenses/by/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_nd:
		name='Creative Commons Attribution-NoDerivs 2.0'
		shortname='Attribution-NoDerivs'
		abbreviation = 'by-nd/2.0'
		link = 'http://creativecommons.org/licenses/by-nd/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nd/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'
		shareable = True
    class by_nc_nd:
		name='Creative Commons Attribution-NonCommercial-NoDerivs 2.0'
		shortname='Attribution-NonCommercial-NoDerivs'
		abbreviation = 'by-nc-nd/2.0'
		link = 'http://creativecommons.org/licenses/by-nc-nd/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc-nd/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use the work for commercial purposes.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'
		shareable = True
    class bc_nc:
		name='Creative Commons Attribution-NonCommercial 2.0'
		shortname='Attribution-NonCommercial'
		abbreviation = 'bc-nc/2.0'
		link = 'http://creativecommons.org/licenses/by-nc/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_nc_sa:
		name='Creative Commons Attribution-NonCommercial-ShareAlike 2.0'
		shortname='Attribution-ShareAlike'
		abbreviation = 'by-nc-sa/2.0'
		link = 'http://creativecommons.org/licenses/by-nc-sa/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc-sa/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_sa:
		name='Creative Commons Attribution-ShareAlike 2.0'
		shortname='Public Domain'
		abbreviation = 'by-sa/2.0'
		link = 'http://creativecommons.org/licenses/by-sa/2.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-sa/2.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of this work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'
		shareable = True
    class pd:
		name='Public Domain'
		shortname=''
		abbreviation = 'pd'
		link = 'http://creativecommons.org/licenses/publicdomain/'
		thumbnail = 'http://mirrors.creativecommons.org/presskit/icons/pd.png'
		description = '<p>By placing a work in the public domain you are disclaiming all copyright to the work for the benefit of the public at large.</p><p>Once placed in the public domain, the Work may be freely reproduced, distributed, transmitted, used, modified, built upon, or otherwise exploited by anyone for any purpose, commercial or non-commercial, and in any way, including by methods that have not yet been invented or conceived.</p>'
		shareable = True
    class by_3:
		name='Creative Commons Attribution 3.0'
		shortname='Attribution'
		abbreviation = 'by/3.0'
		link = ''
		thumbnail = 'http://i.creativecommons.org/l/by/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_nd_3:
		name='Creative Commons Attribution-NoDerivs 3.0'
		shortname='Attribution-NoDerivs'
		abbreviation = 'by-nd/3.0'
		link = 'http://creativecommons.org/licenses/by-nd/3.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nd/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make commercial use of the work</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'
		shareable = True
    class by_nc_nd_3:
		name='Creative Commons Attribution-NonCommercial-NoDerivs 3.0'
		shortname='Attribution-NonCommercial-NoDerivs'
		abbreviation = 'by-nc-nd/3.0'
		link = 'http://creativecommons.org/licenses/by-nc-nd/3.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use the work for commercial purposes.</li><li>Make clear the original license terms.</li><li>Do not alter, transform, or build upon this work.</li></ul>'
		shareable = True
    class by_nc_3:
		name='Creative Commons Attribution-NonCommercial 3.0'
		shortname='Attribution-NonCommercial'
		abbreviation = 'by-nc/3.0'
		link = 'http://creativecommons.org/licenses/by-nc/3.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_nc_sa_3:
		name='Creative Commons Attribution-NonCommercial-ShareAlike 3.0'
		shortname='Attribution-ShareAlike'
		abbreviation = 'by-nc-sa/3.0'
		link = 'http://creativecommons.org/licenses/by-nc-sa/3.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nc=sa/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Do not use this work for commercial purposes.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'
		shareable = True
    class by_nd_4:
		name='Creative Commons Attribution-ShareAlike 3.0'
		shortname='Public Domain'
		abbreviation = 'by-nd/3.0'
		link = 'http://creativecommons.org/licenses/by-sa/3.0/'
		thumbnail = 'http://i.creativecommons.org/l/by-nd/3.0/88x31.png'
		description = '<p>Others are free to:</p> <ul><li>copy, distribute, display and perform the work;</li><li>make derivative works;</li><li>make commercial use of this work;</li></ul><p>As long as they:</p><ul><li>Give the original author credit.</li><li>Share alike &#151; if they alter, transform, or build upon this work they must distribute the resulting work under a license identical to this one.<li>Make clear the original license terms.</li></ul>'
		shareable = True

import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(globals()["__file__"])),'../../../'))
from hackertalks.model import meta
from hackertalks.model import meta
from hackertalks import model
from fixture.style import NamedDataStyle
from fixture import SQLAlchemyFixture

def get_db():
    return SQLAlchemyFixture(env=model, style=NamedDataStyle(),engine=meta.engine)

def load_data(cls):
    print cls
    try:
        get_db().data(cls).setup()
    except Exception, e:
        print e
    meta.Session.commit()

#def load_all(): # may be misguided, use load_data(TalkData) instead
#    g = globals().items()
#    [load_data(x[1]) for x in g if isclass(x[1]) and issubclass(x[1], DataSet) and not x[1]==DataSet];
