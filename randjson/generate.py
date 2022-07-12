import random, time, json, re, os, sys
from sentence import Sentence

dir_name = os.path.dirname(os.path.abspath(__file__))

def load_file(filename):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


class RandomDate:
    format = "%m/%d/%Y"

    def __init__(self):
        pass

    @staticmethod
    def generate():
        now = random.randint(0, int(time.time()))
        return time.strftime(RandomDate.format, time.localtime(now))

    @staticmethod
    def generate_between(start, end):
        start = time.mktime(time.strptime(start, RandomDate.format))
        end = time.mktime(time.strptime(end, RandomDate.format))
        if start > end:
            now = random.randint(int(end), int(start))
        else:
            now = random.randint(int(start), int(end))
        return time.strftime(RandomDate.format, time.localtime(now))


class RandomPhone:
    def __init__(self):
        pass

    @staticmethod
    def generate():
        return "({}) {}-{}".format(random.randint(200, 798), random.randint(300,999), random.randint(2000, 9000))


class RandomFirstname:
    filename = '{}/assets/firstname.txt'.format(dir_name)
    names = load_file(filename)

    @staticmethod
    def generate():
        return RandomFirstname.names[random.randrange(0, len(RandomFirstname.names))].title()


class RandomLastname:
    filename = '{}/assets/lastname.txt'.format(dir_name)
    names = load_file(filename)

    @staticmethod
    def generate():
        return RandomLastname.names[random.randrange(0, len(RandomLastname.names))].title()


class RandomNoun:
    filename = '{}/assets/noun.txt'.format(dir_name)
    nouns = load_file(filename)

    @staticmethod
    def generate():
        return RandomNoun.nouns[random.randrange(0, len(RandomNoun.nouns))].title()


class RandomAdjective:
    filename = '{}/assets/adjective.txt'.format(dir_name)
    adjectives = load_file(filename)

    @staticmethod
    def generate():
        return RandomAdjective.adjectives[random.randrange(0, len(RandomAdjective.adjectives))].title()

class RandomColor:
    filename = '{}/assets/colors.txt'.format(dir_name)
    colors = load_file(filename)

    @staticmethod
    def generate():
        return RandomColor.colors[random.randrange(0, len(RandomColor.colors))].title()


class RandomPhrases:
    filename = '{}/assets/phrase.txt'.format(dir_name)
    phrases = load_file(filename)

    @staticmethod
    def generate():
        return RandomPhrases.phrases[random.randrange(0, len(RandomPhrases.phrases))].title()

class RandomSentence:
    sentence = Sentence()

    @staticmethod
    def generate():
        """ Returns a random sentence. """
        return RandomSentence.sentence.random_sentence()


class RandomStreet:
    type =['Street', 'Drive', 'Avenue', 'Road']

    def __init__(self):
        pass

    @staticmethod
    def generate():
        return "{} {} {}".format(random.randint(100,10000),
                                 RandomNoun.generate(),
                                 RandomStreet.type[random.randrange(0, len(RandomStreet.type))])


class RandomCity:
    filename = '{}/assets/city.txt'.format(dir_name)

    def __init__(self):
        self._cities = load_file(self.filename)
        self.cities = []
        for city in self._cities:
            l = city.split(',')
            self.cities.append({
                'city': l[0].strip(),
                'state': l[1].strip(),
                'zip': l[2].strip()
            })

    def generate(self):
        """ Returns a random city, state and zip code in JSON """
        return self.cities[random.randrange(0, len(self.cities))]


class Driver:
    def __init__(self, template):
        self.random_city = RandomCity()
        self.city_map = {}
        self.template = template

    # TODO - broken
    def replace(self, value):
        new_value = []
        for word in re.findall(r'\S+', value):
            new_value.append(self._replace(word))
        return ' '.join(map(str, new_value))

    def _replace(self, random_type):
        """ assumes term begins with __RANDOM__ """
        if not random_type.startswith("__RANDOM__"):
            return random_type

        try:
            terms = random_type.split("__")
            type = terms[2]
            if type.lower() == 'city':
                if len(terms) > 3:
                    if terms[3] in self.city_map:
                        return self.city_map[terms[3]]['city']
                    city_dict = self.random_city.generate()
                    self.city_map[terms[3]] = city_dict
                    return city_dict['city']
                if 'single' in self.city_map:
                    return self.city_map['single']['city']
                self.city_map['single'] = self.random_city.generate()
                return self.city_map['single']['city']
            elif type.lower() == 'zip':
                if len(terms) > 3:
                    if terms[3] in self.city_map:
                        return self.city_map[terms[3]]['zip']
                    city_dict = self.random_city.generate()
                    self.city_map[terms[3]] = city_dict
                    return city_dict['zip']
                if 'single' in self.city_map:
                    return self.city_map['single']['zip']
                self.city_map['single'] = self.random_city.generate()
                return self.city_map['single']['zip']
            elif type.lower() == 'state':
                if len(terms) > 3:
                    if terms[3] in self.city_map:
                        return self.city_map[terms[3]]['state']
                    city_dict = self.random_city.generate()
                    self.city_map[terms[3]] = city_dict
                    return city_dict['state']
                if 'single' in self.city_map:
                    return self.city_map['single']['state']
                self.city_map['single'] = self.random_city.generate()
                return self.city_map['single']['state']
            elif type.lower() == 'street':
                return RandomStreet.generate()
            elif type.lower() == 'phone':
                return RandomPhone.generate()
            elif type.lower() == 'firstname':
                return RandomFirstname.generate()
            elif type.lower() == 'lastname':
                return RandomLastname.generate()
            elif type.lower() == 'number':
                if len(terms) > 3:
                    return random.randint(int(terms[3]), int(terms[4]))
                return random.randint(0,5000)
            elif type.lower() == 'money':
                if len(terms) > 3:
                    return random.uniform(int(terms[3]), int(terms[4]))
                return random.uniform(0,10000000)
            elif type.lower() == 'date':
                if len(terms) > 3:
                    return RandomDate.generate_between(terms[3], terms[4])
                return RandomDate.generate()
            elif type.lower() == 'phrase':
                return RandomPhrases.generate()
            elif type.lower() == 'sentence':
                return RandomSentence.generate()
            elif type.lower() == 'noun':
                return RandomNoun.generate()
            elif type.lower() == 'adjective':
                return RandomAdjective.generate()
            elif type.lower() == 'color':
                return RandomColor.generate()
            elif type.lower() == 'choice':
                return random.choice(terms[3:])
        except Exception as e:
            return "error on {}".format(random_type)

        return random_type

    def get(self, number):
        result = []
        for a in range(number):
            template = json.loads(self.template)
            result.append(self.generate(template))
            self.reset()
        return result

    def reset(self):
        self.random_city = RandomCity()
        self.city_map = {}

    def generate(self, template):
        """ template is a json object """
        if type(template) is str:
            return self.replace(template)
        if type(template) is list:
            newlist = []
            for item in template:
                newlist.append(self.generate(item))
            return newlist

        for key in template:
            if type(template[key]) is str and template[key].startswith("__RANDOM__"):
                template[key] = self.replace(template[key])
            elif type(template[key]) is list:
                newlist = []
                for item in template[key]:
                    newlist.append(self.generate(item))
                template[key] = self.generate(template[key])
            elif type(template[key]) is dict:
                template[key] = self.generate(template[key])
        return template


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: {} template_file".format(sys.argv[0]), file=sys.stderr)
        exit(1)
    filename = sys.argv[1]

    if len(sys.argv) > 2:
        count = int(sys.argv[2])
    else:
        count = 1
    with open(filename, "r") as file:
        template = file.read()
    driver = Driver(template)
    print(json.dumps(driver.get(count)))
