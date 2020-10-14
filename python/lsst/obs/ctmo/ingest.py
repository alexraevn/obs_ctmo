from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time


def datetime2mjd(date_time):
    "Convert a datetime object into Modified Julian Date"
    YY = date_time.year
    MO = date_time.month
    DD = date_time.day
    HH = date_time.hour
    MI = date_time.minute
    SS = date_time.second

    if MO == 1 or MO == 2:
        mm = MO + 12
        yy = YY - 1
    else:
        mm = MO
        yy = YY

    dd = DD + (HH/24.0 + MI/24.0/60.0 + SS/24.0/3600.0)

    A = int(365.25*yy)
    B = int(yy/400.0)
    C = int(yy/100.0)
    D = int(30.59*(mm-2))

    mjd = A + B - C + D + dd - 678912

    return mjd


class CtmoCameraParseTask(ParseTask):
    """[From https://github.com/lsst/obs_lsst/blob/f0c4ae506e8e0a85789aebdd970d7e704c9c6e24/
    python/lsst/obs/lsst/ingest.py#L54]:
    All translator methods receive the header metadata [here via "md"] and
    should return the appropriate value, or None if the value cannot be determined. 
    """

    def translateDate(self, md):
        """Take date in FITS header in format yyyymmdd,
        and convert to yyyy-mm-dd.

        This isn't strictly necessary, but it's a good example of what a
        translate script can be used for."""

        date = md.get("DATE-OBS")
        date = [date[0:4], date[4:6], date[6:]]
        date = '-'.join(date)
        t = Time(date, format='iso', out_subfmt='date').iso
        return t
     
    def translateVisit(self, md):
        "Convert string 'visit' from FITS header into integer"
        return int(md.get("RUN")) 
                    
    def translateCcd(self, md):
        "Convert string 'ccd' from FITS header into integer"
        return int(md.get("DETECTOR"))

    def translateExpTime(self, md):
        "Convert string 'expTime' from FITS header into float"
        return float(md.get("EXPTIME"))  