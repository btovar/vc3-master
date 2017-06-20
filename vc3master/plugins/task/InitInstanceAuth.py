#!/usr/bin/env python
# 
#
import json

from vc3master.task import VC3Task

class InitInstanceAuth(VC3Task):
    '''
    Plugin to do first-time overall VC3 instance setup. 
    Confirm that CA exists, create host cert for this server. 
     
     
    { "vc3": {
        "ca-chain" : "<base64encoded ca chain file>"
        
        }
    }
     
    '''    
    def runtask(self):
        '''
        '''
        self.log.info("Running task %s" % self.section)
        self.log.debug("Getting 'vc3' doc.")
        try:
            doc = self.parent.parent.infoclient.getdocument('vc3')
            self.log.debug('Doc is %s' % doc)
        except Exception as e:
            self.log.error("Exception: %s" % e)

        if doc is not None:            
            try:
                ds = json.loads(doc)
                try:
                    requests = ds['vc3']
                    self.log.debug("vc3 section already in doc. Doing nothing.")
                except KeyError:
                    # no vc3 section
                    self.log.debug("No vc3 section in doc.")
                    ccstr = self.parent.parent.ssca.getcertchain()
                    eccstr = self.parent.parent.infoclient.encode(ccstr)
                    ds['vc3'] = { "ca-chain" : eccstr, 
                                  "encoding" : "base64" }
                    jd = json.dumps(ds)
                    self.parent.parent.infoclient.storedocument('vc3',jd)
            except Exception as e:
                self.log.error("Exception: %s" % e)
        
            