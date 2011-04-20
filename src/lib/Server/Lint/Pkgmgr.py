import Bcfg2.Server.Lint

class Pkgmgr(Bcfg2.Server.Lint.ServerPlugin):
    """ find duplicate Pkgmgr entries with the same priority """

    @Bcfg2.Server.Lint.returnErrors
    def Run(self):
        pset = set()
        for plist in self.core.plugins['Pkgmgr'].entries.values():
            if self.HandlesFile(plist.name):
                xdata = plist.data
                # get priority, type, group
                priority = xdata.getroot().get('priority')
                ptype = xdata.getroot().get('type')
                for pkg in xdata.findall("//Package"):
                    if pkg.getparent().tag == 'Group':
                        grp = pkg.getparent().get('name')
                        if (type(grp) is not str and
                            grp.getparent().tag == 'Group'):
                            pgrp = grp.getparent().get('name')
                        else:
                            pgrp = 'none'
                    else:
                        grp = 'none'
                        pgrp = 'none'
                    ptuple = (pkg.get('name'), priority, ptype, grp, pgrp)
                    # check if package is already listed with same
                    # priority, type, grp
                    if ptuple in pset:
                        self.LintWarning("Duplicate Package %s, priority:%s, type:%s" %
                                         (pkg.get('name'), priority, ptype))
                    else:
                        pset.add(ptuple)
