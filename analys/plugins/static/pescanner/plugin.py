import re
import pescanner
from analys.plugins.plugin import Plugin

class AnalysPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super(AnalysPlugin, self).__init__(*args, **kwargs)

    def submit(self):
        result = pescanner.PEScanner([self.get_resource().create_temp_file()], '', '').collect()

        head = result[:7]

        for i, x in enumerate(result):
          if '-------' in x:
              bodystart = i + 1
              break

        try:
          bodyend = [i for i,x in enumerate(result) if 'Version info' in x][0]
          final  = ''.join(result[bodyend+1:]).split('\n')

        except:
          bodyend = len(result)
          final = False

        sections = result[bodystart:bodyend]

        result = {}
        result['Body'] = {}
        result['Version info'] = {}

        for h in head:
          result['Body'][h.split(':')[0]] = re.sub('  +','',h.split(': ')[1])
        if final:
          for f in final:
              result['Version info'][f.split(':')[0]] = f.split(':')[1]

        result['Sections']=[]

        for b in sections:
          b=b.split()
          parts = ['Name', 'VirtAddr', 'VirtSize', 'RawSize', 'Entropy', 'Suspicious']
          subresult = {}
          if b:
              parts = parts[:len(b)]
              subresult = dict(zip(parts, b))
              result['Sections'].append(subresult)

        self.insert(result)
        return True

        def render(self):
            pass
