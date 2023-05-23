import re

class ReplaceSubstring:
    def __init__(self, txt=''):
        self.txt = txt

    def replace_sub_str(self):
        input_query_txt = self.txt
        # input_query_txt = re.sub(r'\ba week ago\b', 'lastweek', input_query_txt)
        # input_query_txt = re.sub(r'\bone week ago\b', 'lastweek', input_query_txt)
        # input_query_txt = re.sub(r'\blast week\b', 'lastweek', input_query_txt)
        input_query_txt = re.sub(r'\band on december\b', 'and date is december', input_query_txt)
        input_query_txt = re.sub(r'\band on november\b', 'and date is november', input_query_txt)
        input_query_txt = re.sub(r'\band on october\b', 'and date is october', input_query_txt)
        input_query_txt = re.sub(r'\band on september\b', 'and date is september', input_query_txt)
        input_query_txt = re.sub(r'\band on august\b', 'and date is august', input_query_txt)
        input_query_txt = re.sub(r'\band on july\b', 'and date is july', input_query_txt)
        input_query_txt = re.sub(r'\band on june\b', 'and date is june', input_query_txt)
        input_query_txt = re.sub(r'\band on may\b', 'and date is may', input_query_txt)
        input_query_txt = re.sub(r'\band on april\b', 'and date is april', input_query_txt)
        input_query_txt = re.sub(r'\band on march\b', 'and date is march', input_query_txt)
        input_query_txt = re.sub(r'\band on february\b', 'and date is february', input_query_txt)
        input_query_txt = re.sub(r'\band on january\b', 'and date is january', input_query_txt) 

        input_query_txt = re.sub(r'\band december\b', 'and date is not above december', input_query_txt)
        input_query_txt = re.sub(r'\band november\b', 'and date is not above november', input_query_txt)
        input_query_txt = re.sub(r'\band october\b', 'and date is not above october', input_query_txt)
        input_query_txt = re.sub(r'\band september\b', 'and date is not above september', input_query_txt)
        input_query_txt = re.sub(r'\band august\b', 'and date is not above august', input_query_txt)
        input_query_txt = re.sub(r'\band july\b', 'and date is not above july', input_query_txt)
        input_query_txt = re.sub(r'\band june\b', 'and date is not above june', input_query_txt)
        input_query_txt = re.sub(r'\band may\b', 'and date is not above may', input_query_txt)
        input_query_txt = re.sub(r'\band april\b', 'and date is not above april', input_query_txt)
        input_query_txt = re.sub(r'\band march\b', 'and date is not above march', input_query_txt)
        input_query_txt = re.sub(r'\band february\b', 'and date is not above february', input_query_txt)
        input_query_txt = re.sub(r'\band january\b', 'and date is not above january', input_query_txt) 

        input_query_txt = re.sub(r'\bto december\b', 'and date is not above december', input_query_txt)
        input_query_txt = re.sub(r'\bto november\b', 'and date is not above november', input_query_txt)
        input_query_txt = re.sub(r'\bto october\b', 'and date is not above october', input_query_txt)
        input_query_txt = re.sub(r'\bto september\b', 'and date is not above september', input_query_txt)
        input_query_txt = re.sub(r'\bto august\b', 'and date is not above august', input_query_txt)
        input_query_txt = re.sub(r'\bto july\b', 'and date is not above july', input_query_txt)
        input_query_txt = re.sub(r'\bto june\b', 'and date is not above june', input_query_txt)
        input_query_txt = re.sub(r'\bto may\b', 'and date is not above may', input_query_txt)
        input_query_txt = re.sub(r'\bto april\b', 'and date is not above april', input_query_txt)
        input_query_txt = re.sub(r'\bto march\b', 'and date is not above march', input_query_txt)
        input_query_txt = re.sub(r'\bto february\b', 'and date is not above february', input_query_txt)
        input_query_txt = re.sub(r'\bto january\b', 'and date is not above january', input_query_txt) 

        input_query_txt = re.sub(r'\buntil december\b', 'and date is not above december', input_query_txt)
        input_query_txt = re.sub(r'\buntil november\b', 'and date is not above november', input_query_txt)
        input_query_txt = re.sub(r'\buntil october\b', 'and date is not above october', input_query_txt)
        input_query_txt = re.sub(r'\buntil september\b', 'and date is not above september', input_query_txt)
        input_query_txt = re.sub(r'\buntil august\b', 'and date is not above august', input_query_txt)
        input_query_txt = re.sub(r'\buntil july\b', 'and date is not above july', input_query_txt)
        input_query_txt = re.sub(r'\buntil june\b', 'and date is not above june', input_query_txt)
        input_query_txt = re.sub(r'\buntil may\b', 'and date is not above may', input_query_txt)
        input_query_txt = re.sub(r'\buntil april\b', 'and date is not above april', input_query_txt)
        input_query_txt = re.sub(r'\buntil march\b', 'and date is not above march', input_query_txt)
        input_query_txt = re.sub(r'\buntil february\b', 'and date is not above february', input_query_txt)
        input_query_txt = re.sub(r'\buntil january\b', 'and date is not above january', input_query_txt) 

        input_query_txt = re.sub(r'\bwithin dates december\b', 'and date is not below december', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates november\b', 'and date is not below november', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates october\b', 'and date is not below october', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates september\b', 'and date is not below september', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates august\b', 'and date is not below august', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates july\b', 'and date is not below july', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates june\b', 'and date is not below june', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates may\b', 'and date is not below may', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates april\b', 'and date is not below april', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates march\b', 'and date is not below march', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates february\b', 'and date is not below february', input_query_txt)
        input_query_txt = re.sub(r'\bwithin dates january\b', 'and date is not below january', input_query_txt) 

        input_query_txt = re.sub(r'\bwithin december\b', 'and date is not below december', input_query_txt)
        input_query_txt = re.sub(r'\bwithin november\b', 'and date is not below november', input_query_txt)
        input_query_txt = re.sub(r'\bwithin october\b', 'and date is not below october', input_query_txt)
        input_query_txt = re.sub(r'\bwithin september\b', 'and date is not below september', input_query_txt)
        input_query_txt = re.sub(r'\bwithin august\b', 'and date is not below august', input_query_txt)
        input_query_txt = re.sub(r'\bwithin july\b', 'and date is not below july', input_query_txt)
        input_query_txt = re.sub(r'\bwithin june\b', 'and date is not below june', input_query_txt)
        input_query_txt = re.sub(r'\bwithin may\b', 'and date is not below may', input_query_txt)
        input_query_txt = re.sub(r'\bwithin april\b', 'and date is not below april', input_query_txt)
        input_query_txt = re.sub(r'\bwithin march\b', 'and date is not below march', input_query_txt)
        input_query_txt = re.sub(r'\bwithin february\b', 'and date is not below february', input_query_txt)
        input_query_txt = re.sub(r'\bwithin january\b', 'and date is not below january', input_query_txt) 

        input_query_txt = re.sub(r'\bbetween december\b', 'and date is not below december', input_query_txt)
        input_query_txt = re.sub(r'\bbetween november\b', 'and date is not below november', input_query_txt)
        input_query_txt = re.sub(r'\bbetween october\b', 'and date is not below october', input_query_txt)
        input_query_txt = re.sub(r'\bbetween september\b', 'and date is not below september', input_query_txt)
        input_query_txt = re.sub(r'\bbetween august\b', 'and date is not below august', input_query_txt)
        input_query_txt = re.sub(r'\bbetween july\b', 'and date is not below july', input_query_txt)
        input_query_txt = re.sub(r'\bbetween june\b', 'and date is not below june', input_query_txt)
        input_query_txt = re.sub(r'\bbetween may\b', 'and date is not below may', input_query_txt)
        input_query_txt = re.sub(r'\bbetween april\b', 'and date is not below april', input_query_txt)
        input_query_txt = re.sub(r'\bbetween march\b', 'and date is not below march', input_query_txt)
        input_query_txt = re.sub(r'\bbetween february\b', 'and date is not below february', input_query_txt)
        input_query_txt = re.sub(r'\bbetween january\b', 'and date is not below january', input_query_txt) 

        input_query_txt = re.sub(r'\bfrom december\b', 'and date is not below december', input_query_txt)
        input_query_txt = re.sub(r'\bfrom november\b', 'and date is not below november', input_query_txt)
        input_query_txt = re.sub(r'\bfrom october\b', 'and date is not below october', input_query_txt)
        input_query_txt = re.sub(r'\bfrom september\b', 'and date is not below september', input_query_txt)
        input_query_txt = re.sub(r'\bfrom august\b', 'and date is not below august', input_query_txt)
        input_query_txt = re.sub(r'\bfrom july\b', 'and date is not below july', input_query_txt)
        input_query_txt = re.sub(r'\bfrom june\b', 'and date is not below june', input_query_txt)
        input_query_txt = re.sub(r'\bfrom may\b', 'and date is not below may', input_query_txt)
        input_query_txt = re.sub(r'\bfrom april\b', 'and date is not below april', input_query_txt)
        input_query_txt = re.sub(r'\bfrom march\b', 'and date is not below march', input_query_txt)
        input_query_txt = re.sub(r'\bfrom february\b', 'and date is not below february', input_query_txt)
        input_query_txt = re.sub(r'\bfrom january\b', 'and date is not below january', input_query_txt) 

        input_query_txt = re.sub(r'\bon december\b', 'and date is december', input_query_txt)
        input_query_txt = re.sub(r'\bon november\b', 'and date is november', input_query_txt)
        input_query_txt = re.sub(r'\bon october\b', 'and date is october', input_query_txt)
        input_query_txt = re.sub(r'\bon september\b', 'and date is september', input_query_txt)
        input_query_txt = re.sub(r'\bon august\b', 'and date is august', input_query_txt)
        input_query_txt = re.sub(r'\bon july\b', 'and date is july', input_query_txt)
        input_query_txt = re.sub(r'\bon june\b', 'and date is june', input_query_txt)
        input_query_txt = re.sub(r'\bon may\b', 'and date is may', input_query_txt)
        input_query_txt = re.sub(r'\bon april\b', 'and date is april', input_query_txt)
        input_query_txt = re.sub(r'\bon march\b', 'and date is march', input_query_txt)
        input_query_txt = re.sub(r'\bon february\b', 'and date is february', input_query_txt)
        input_query_txt = re.sub(r'\bon january\b', 'and date is january', input_query_txt)
        input_query_txt = re.sub(r'\bwhere date is\b', 'and date is', input_query_txt)
        input_query_txt = re.sub(r'\bwhere date\b', 'and date is', input_query_txt)
        input_query_txt = re.sub(r'\ba day ago\b', 'yesterday', input_query_txt)
        input_query_txt = re.sub(r'\bone day ago\b', 'yesterday', input_query_txt)
        input_query_txt = re.sub(r'\b1 day ago\b', 'yesterday', input_query_txt)
        input_query_txt = re.sub(r'\boptimal\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\bcore\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\bideal\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\boptimal\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\bbest\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\bcondition\b', 'optimum', input_query_txt)
        input_query_txt = re.sub(r'\bcrop\b', 'plant', input_query_txt)
        input_query_txt = re.sub(r'\bcrops\b', 'plant', input_query_txt)
        input_query_txt = re.sub(r'\bfarm\b', 'plant', input_query_txt)
        input_query_txt = re.sub(r'\blist\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bdisplay\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bview\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bshow me\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bpresent\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bexhibit\b', 'show', input_query_txt)
        input_query_txt = re.sub(r'\bshow data\b', ' show all', input_query_txt)
        input_query_txt = re.sub(r'\bshow data\b', ' show all', input_query_txt)
        input_query_txt = re.sub(r'\bthe\b', '', input_query_txt)
        input_query_txt = re.sub(r'\bevery single\b', ' all', input_query_txt)
        input_query_txt = re.sub(r'\beach of plants\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\beach of plant\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\beach plants\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\beach plant\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\bany of plants\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\bany of plant\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\bany plants\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\bany plant\b', ' of all plant', input_query_txt)
        input_query_txt = re.sub(r'\bany of data\b', ' all', input_query_txt)
        input_query_txt = re.sub(r'\bsee\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bacquire\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bobtain\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bexhibit\b', ' show', input_query_txt)
        input_query_txt = re.sub(r'\bplants\b', 'table', input_query_txt)
        input_query_txt = re.sub(r'\bplant\b', 'table', input_query_txt)
        input_query_txt = re.sub(r'\btables\b', 'table', input_query_txt)
        input_query_txt = re.sub(r'\bbut is not ranging from\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut not ranging from\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut not including\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut leaving out\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut other than\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut excluding\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut omitting\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut except\b', 'and not', input_query_txt)
        input_query_txt = re.sub(r'\bbut\b', 'and', input_query_txt)
        input_query_txt = input_query_txt.replace('in the range of', ' between')
        input_query_txt = input_query_txt.replace('in the range', ' between')
        input_query_txt = input_query_txt.replace('ranging from', ' between')
        input_query_txt = input_query_txt.replace('ranges from', ' between')
        input_query_txt = input_query_txt.replace('through', ' between')
        input_query_txt = input_query_txt.replace('within', ' between')
        input_query_txt = input_query_txt.replace('greater than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('larger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('bigger than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('higher than or equal', ' above equal')
        input_query_txt = input_query_txt.replace('lesser than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('smaller than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('less than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('lower than or equal', ' below equal')
        input_query_txt = input_query_txt.replace('on condition', ' where')
        input_query_txt = input_query_txt.replace('on assumption', ' where')
        input_query_txt = input_query_txt.replace('above or equal', ' above equal')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('beyond or over', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('over and beyond', ' above')
        input_query_txt = input_query_txt.replace('below or equal', ' below equal')
        input_query_txt = input_query_txt.replace('on or before', ' below equal')
        input_query_txt = input_query_txt.replace('on or after', ' above equal')
        input_query_txt = input_query_txt.replace('before or on', ' below equal')
        input_query_txt = input_query_txt.replace('after or on', ' above equal')
        input_query_txt = input_query_txt.replace('each and every', ' all')
        input_query_txt = input_query_txt.replace('this day', ' today')
        input_query_txt = input_query_txt.replace('in which', ' where')
        input_query_txt = input_query_txt.replace('at which', ' where')
        input_query_txt = input_query_txt.replace('higher than', ' above')
        input_query_txt = input_query_txt.replace('greater than', ' above')
        input_query_txt = input_query_txt.replace('larger than', ' below')
        input_query_txt = input_query_txt.replace('bigger than', ' above')
        input_query_txt = input_query_txt.replace('lesser than', ' below')
        input_query_txt = input_query_txt.replace('smaller than', ' below')
        input_query_txt = input_query_txt.replace('less than', ' below')
        input_query_txt = input_query_txt.replace('lower than', ' below')
        input_query_txt = input_query_txt.replace('sensors nodes', ' data')
        input_query_txt = input_query_txt.replace('sensor nodes', ' data')
        input_query_txt = input_query_txt.replace('sensors node', ' data')
        input_query_txt = input_query_txt.replace('sensor node', ' data')
        input_query_txt = input_query_txt.replace('sensors data', ' data')
        input_query_txt = input_query_txt.replace('sensor data', ' data')
        input_query_txt = input_query_txt.replace('sensors reading', ' data')
        input_query_txt = input_query_txt.replace('sensor reading', ' data')
        input_query_txt = input_query_txt.replace('sensors readings', ' data')
        input_query_txt = input_query_txt.replace('sensor readings', ' data')
        input_query_txt = input_query_txt.replace('°', ' degree')
        input_query_txt = input_query_txt.replace('degrees', ' degree')
        input_query_txt = input_query_txt.replace('%', ' percent')
        input_query_txt = input_query_txt.replace('greater', ' above')
        input_query_txt = input_query_txt.replace('larger', ' above')
        input_query_txt = input_query_txt.replace('higher', ' above')
        input_query_txt = input_query_txt.replace('over', ' above')
        input_query_txt = input_query_txt.replace('beyond', ' above')
        input_query_txt = input_query_txt.replace('exceeding', ' above')
        input_query_txt = input_query_txt.replace('bigger', ' above')
        input_query_txt = input_query_txt.replace('exceeds', ' above')
        input_query_txt = input_query_txt.replace('exceed', ' above')
        input_query_txt = input_query_txt.replace('after', ' above')
        input_query_txt = input_query_txt.replace('lesser', ' below')
        input_query_txt = input_query_txt.replace('less', ' below')
        input_query_txt = input_query_txt.replace('smaller', ' below')
        input_query_txt = input_query_txt.replace('lower', ' below')
        input_query_txt = input_query_txt.replace('before', ' below')
        input_query_txt = input_query_txt.replace('not including', ' not')
        input_query_txt = input_query_txt.replace('not inclusive', ' not')
        input_query_txt = input_query_txt.replace('leaving out', ' not')
        input_query_txt = input_query_txt.replace('other than', ' not')
        input_query_txt = input_query_txt.replace('excluding', ' not')
        input_query_txt = input_query_txt.replace('omitting', ' not')
        input_query_txt = input_query_txt.replace('except', ' not')
        input_query_txt = input_query_txt.replace('wherein', ' where')
        input_query_txt = input_query_txt.replace('which', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('whose', ' where')
        input_query_txt = input_query_txt.replace('if', ' where')
        input_query_txt = input_query_txt.replace('provided', ' where')
        input_query_txt = input_query_txt.replace('assuming', ' where')
        input_query_txt = input_query_txt.replace('supposing', ' where')
        input_query_txt = input_query_txt.replace('presuming', ' where')
        input_query_txt = input_query_txt.replace('that', ' where')
        input_query_txt = input_query_txt.replace('from', ' of')
        input_query_txt = input_query_txt.replace('each', ' all')
        input_query_txt = input_query_txt.replace('every', ' all')
        input_query_txt = input_query_txt.replace('entire', ' all')
        input_query_txt = input_query_txt.replace('everything', ' all')
        input_query_txt = input_query_txt.replace('check', ' show')
        input_query_txt = input_query_txt.replace('provide', ' show')
        input_query_txt = input_query_txt.replace('graph', ' show date ')
        input_query_txt = input_query_txt.replace('inspect', ' show')
        input_query_txt = input_query_txt.replace('scan', ' show')
        input_query_txt = input_query_txt.replace('parameters', ' data')
        input_query_txt = input_query_txt.replace('parameter', ' data')
        input_query_txt = input_query_txt.replace('readings', ' data')
        input_query_txt = input_query_txt.replace('reading', ' data')
        input_query_txt = input_query_txt.replace('sensors', ' data')
        input_query_txt = input_query_txt.replace('sensor', ' data')
        input_query_txt = input_query_txt.replace('for', ' of')
        input_query_txt = input_query_txt.replace('me', '')
        input_query_txt = input_query_txt.replace('lakhs', ' lux')
        input_query_txt = input_query_txt.replace('lakhs', ' lux')
        input_query_txt = input_query_txt.replace('looks', ' lux')
        input_query_txt = input_query_txt.replace('blocks', ' lux')
        input_query_txt = input_query_txt.replace('bpm', ' ppm')
        input_query_txt = re.sub(r' +', ' ', input_query_txt)
        input_query_txt = re.sub(r'\ball data\b', 'all of data', input_query_txt)
        input_query_txt = re.sub(r'\ball of date\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\ball of date\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\ball of temperature\b', 'temperature', input_query_txt)
        input_query_txt = re.sub(r'\ball of humidity\b', 'humidity', input_query_txt)
        input_query_txt = re.sub(r'\ball of soil\b', 'soil', input_query_txt)
        input_query_txt = re.sub(r'\ball of light\b', 'light', input_query_txt)
        input_query_txt = re.sub(r'\ball of air\b', 'air', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of date\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of temperature\b', 'temperature', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of humidity\b', 'humidity', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of soil\b', 'soil', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of light\b', 'light', input_query_txt)
        input_query_txt = re.sub(r'\ball of data of air\b', 'air', input_query_txt)
        input_query_txt = re.sub(r'\bdata of date\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\bdata of temperature\b', 'temperature', input_query_txt)
        input_query_txt = re.sub(r'\bdata of humidity\b', 'humidity', input_query_txt)
        input_query_txt = re.sub(r'\bdata of soil\b', 'soil', input_query_txt)
        input_query_txt = re.sub(r'\bdata of light\b', 'light', input_query_txt)
        input_query_txt = re.sub(r'\bdata of air\b', 'air', input_query_txt)
        input_query_txt = re.sub(r'\bdata of date\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\btemperature data\b', 'temperature', input_query_txt)
        input_query_txt = re.sub(r'\bhumidity data\b', 'humidity', input_query_txt)
        input_query_txt = re.sub(r'\bsoil data\b', 'soil', input_query_txt)
        input_query_txt = re.sub(r'\blight data\b', 'light', input_query_txt)
        input_query_txt = re.sub(r'\bair data\b', 'air', input_query_txt)
        input_query_txt = re.sub(r'\bdate data\b', 'date', input_query_txt)
        input_query_txt = re.sub(r'\bdata of all\b', ' all', input_query_txt)
        input_query_txt = re.sub(r'\bdata of\b', '', input_query_txt)
        input_query_txt = re.sub(r'\bdata data\b', '', input_query_txt)

        return input_query_txt