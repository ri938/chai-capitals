from collections import defaultdict
import random

from chai_py import ChaiBot, Update
import utils


class Bot(ChaiBot):
    QUESTION_SET = None

    def setup(self):
        self.logger.info("Setting up...")
        self.user_states = defaultdict(dict)
        self.user_correct = defaultdict(list)
        self.user_incorrect = defaultdict(list)
        self.user_counts = defaultdict(int)

    async def on_message(self, update: Update) -> str:
        cid = update.conversation_id
        user_count = self.user_counts[cid]
        states = self._get_state_for_conversation(cid)

        if self.user_counts[cid] == len(states):
            return self._get_conversation_end_response(cid)

        if 'DEBUG' in update.latest_message.text:
            return self._get_debug_data(update)

        msg = ''
        if user_count > 0:
            state, capitol = states[user_count - 1]

            is_correct = utils.check_answer(update.latest_message.text, capitol)

            if is_correct:
                self.user_correct[cid].append(state)
                msg = '🎉 🎉 \nCorrect: '
            else:
                self.user_incorrect[cid].append(state)
                msg = 'Incorrect: '

            msg += 'the capital of {} is {}.'.format(state, capitol)

            num_correct = len(self.user_correct[cid])
            num_incorrect = len(self.user_incorrect[cid])
            msg += '\nYour score is {}/{}.'.format(num_correct, num_correct + num_incorrect)

            # GET BANTER
            banter = ''
            if is_correct:
                if num_correct == 1:
                    banter = 'Well Done!'
                if num_correct == 2:
                    banter = 'Well Done, you superstar!!'
                if num_correct == 3:
                    banter = 'Well Done, you\'re on fire!!'
            else:
                if num_incorrect == 2:
                    banter = 'You wally!'
                if num_incorrect == 3:
                    banter = 'Your IQ is very low!'
                if num_incorrect == 4:
                    banter = 'You really should just give up!'
                if num_incorrect > 4:
                    banter = '🤪'
            msg = banter + '\n' + msg

        state, capitol = states[user_count]
        self.user_counts[cid] += 1

        question = 'What is the capital of {}?'.format(state)
        if msg:
            msg = '{}\n{}'.format(msg, question)
        else:
            msg = question
        return msg

    def _get_conversation_end_response(self, cid):
        num_correct = len(self.user_correct[cid])
        num_incorrect = len(self.user_incorrect[cid])
        total = num_correct + num_incorrect
        msg = 'Well done for completing the quiz. ' \
              'You scored {}/{}'.format(correct, total)
        return msg

    def _get_debug_data(self, update):
        cid = update.conversation_id
        resp = {
            'cid': cid,
            'correct': self.user_correct[cid],
            'incorrect': self.user_incorrect[cid],
            'dict': update.__dict__
        }
        return str(resp)

    def _has_replied_before(self, cid):
        return len(self.user_correct[cid]) + len(self.user_incorrect[cid]) > 0

    def _get_state_for_conversation(self, cid):
        if cid not in self.user_states:
            states = self._get_capitols()
            self.user_states[cid] = states
        return self.user_states[cid]

    def _get_capitols(self):
        questions = list(self.QUESTION_SET.items())
        random.shuffle(questions)
        return questions


class USAStatesQuizBot(Bot):
    QUESTION_SET = {
        'Alabama': 'montgomery',
        'Alaska': 'juneau',
        'Arizona': 'phoenix',
        'Arkansas': 'little rock',
        'California': 'sacramento',
        'Colorado': 'denver',
        'Connecticut': 'hartford',
        'Delaware': 'dover',
        'Florida': 'tallahassee',
        'Georgia': 'atlanta',
        'Hawaii': 'honolulu',
        'Idaho': 'boise',
        'Illinois': 'springfield',
        'Indiana': 'indianapolis',
        'Iowa': 'des moines',
        'Kansas': 'topeka',
        'Kentucky': 'frankfort',
        'Louisiana': 'baton rouge',
        'Maine': 'augusta',
        'Maryland': 'annapolis',
        'Massachusetts': 'boston',
        'Michigan': 'lansing',
        'Minnesota': 'saint paul',
        'Mississippi': 'jackson',
        'Missouri': 'jefferson city',
        'Montana': 'helena',
        'Nebraska': 'lincoln',
        'Nevada': 'carson city',
        'New Hampshire': 'concord',
        'New Jersey': 'trenton',
        'New Mexico': 'santa fe',
        'New York': 'albany',
        'North Carolina': 'raleigh',
        'North Dakota': 'bismarck',
        'Ohio': 'columbus',
        'Oklahoma': 'oklahoma city',
        'Oregon': 'salem',
        'Pennsylvania': 'harrisburg',
        'Rhode Island': 'providence',
        'South Carolina': 'columbia',
        'South Dakota': 'pierre',
        'Tennessee': 'nashville',
        'Texas': 'austin',
        'Utah': 'salt lake city',
        'Vermont': 'montpelier',
        'Virginia': 'richmond',
        'Washington': 'olympia',
        'West Virginia': 'charleston',
        'Wisconsin': 'madison',
        'Wyoming': 'cheyenne'
    }


class EuropeanCapitalsQuizBot(Bot):
    QUESTION_SET = {
        'Albania': 'Tirana',
        'Andorra': 'Andorra la Vella',
        'Armenia': 'Yerevan',
        'Austria': 'Vienna',
        'Belarus': 'Minsk',
        'Belgium': 'Brussels',
        'Bosnia and Herzegovina': 'Sarajevo',
        'Bulgaria': 'Sofia',
        'Croatia': 'Zagreb',
        'Cyprus': 'Nicosia',
        'Czech Republic': 'Prague',
        'Denmark': 'Copenhagen',
        'Estonia': 'Tallinn',
        'Finland': 'Helsinki',
        'France': 'Paris',
        'Georgia': 'Tbilisi',
        'Germany': 'Berlin',
        'Greece': 'Athens',
        'Hungary': 'Budapest',
        'Iceland': 'Reykjavík',
        'Ireland': 'Dublin',
        'Italy': 'Rome',
        'Latvia': 'Riga',
        'Liechtenstein': 'Vaduz',
        'Lithuania': 'Vilnius',
        'Luxembourg': 'Luxembourg',
        'Macedonia': 'Skopje',
        'Malta': 'Valletta',
        'Moldova': 'Chisinau',
        'Monaco': 'Monaco',
        'Montenegro': 'Podgorica',
        'Netherlands': 'Amsterdam',
        'Norway': 'Oslo',
        'Poland': 'Warsaw',
        'Portugal': 'Lisbon',
        'Romania': 'Bucharest',
        'Russia': 'Moscow',
        'San Marino': 'San Marino',
        'Serbia': 'Belgrade',
        'Slovakia': 'Bratislava',
        'Slovenia': 'Ljubljana',
        'Spain': 'Madrid',
        'Sweden': 'Stockholm',
        'Switzerland': 'Bern',
        'Turkey': 'Ankara',
        'Ukraine': 'Kiev',
        'United Kingdom': 'London',
        'Vatican City': 'Vatican City',
    }


class WorldCapitalsQuizBot(Bot):
    QUESTION_SET = {
        'Afghanistan': 'Kabul',
        'Albania': 'Tirana',
        'Algeria': 'Algiers',
        'Andorra': 'Andorra la Vella',
        'Angola': 'Luanda',
        'Antigua and Barbuda': 'Saint Johns',
        'Argentina': 'Buenos Aires',
        'Armenia': 'Yerevan',
        'Australia': 'Canberra',
        'Austria': 'Vienna',
        'Azerbaijan': 'Baku',
        'The Bahamas': 'Nassau',
        'Bahrain': 'Manama',
        'Bangladesh': 'Dhaka',
        'Barbados': 'Bridgetown',
        'Belarus': 'Minsk',
        'Belgium': 'Brussels',
        'Belize': 'Belmopan',
        'Benin': 'Porto-Novo',
        'Bhutan': 'Thimphu',
        'Bolivia': 'La Paz',
        'Bosnia and Herzegovina': 'Sarajevo',
        'Botswana': 'Gaborone',
        'Brazil': 'Brasilia',
        'Brunei': 'Bandar Seri Begawan',
        'Bulgaria': 'Sofia',
        'Burkina Faso': 'Ouagadougou',
        'Burundi': 'Gitega',
        'Cambodia': 'Phnom Penh',
        'Cameroon': 'Yaounde',
        'Canada': 'Ottawa',
        'Cape Verde': 'Praia',
        'Central African Republic': 'Bangui',
        'Chad': 'NDjamena',
        'Chile': 'Santiago',
        'China': 'Beijing',
        'Colombia': 'Bogota',
        'Comoros': 'Moroni',
        'Congo, Republic of the': 'Brazzaville',
        'Congo, Democratic Republic of the': 'Kinshasa',
        'Costa Rica': 'San Jose',
        'Cote d\'Ivoire': 'Yamoussoukro',
        'Croatia': 'Zagreb',
        'Cuba': 'Havana',
        'Cyprus': 'Nicosia',
        'Czech Republic': 'Prague',
        'Denmark': 'Copenhagen',
        'Djibouti': 'Djibouti',
        'Dominica': 'Roseau',
        'Dominican Republic': 'Santo Domingo',
        'East Timor': 'Dili',
        'Ecuador': 'Quito',
        'Egypt': 'Cairo',
        'El Salvador': 'San Salvador',
        'Equatorial Guinea': 'Malabo',
        'Eritrea': 'Asmara',
        'Estonia': 'Tallinn',
        'Ethiopia': 'Addis Ababa',
        'Fiji': 'Suva',
        'Finland': 'Helsinki',
        'France': 'Paris',
        'Gabon': 'Libreville',
        'The Gambia': 'Banjul',
        'Georgia': 'Tbilisi',
        'Germany': 'Berlin',
        'Ghana': 'Accra',
        'Greece': 'Athens',
        'Grenada': 'Saint Georges',
        'Guatemala': 'Guatemala City',
        'Guinea': 'Conakry',
        'Guinea-Bissau': 'Bissau',
        'Guyana': 'Georgetown',
        'Haiti': 'Port-au-Prince',
        'Honduras': 'Tegucigalpa',
        'Hungary': 'Budapest',
        'Iceland': 'Reykjavik',
        'India': 'New Delhi',
        'Indonesia': 'Jakarta',
        'Iran': 'Tehran',
        'Iraq': 'Baghdad',
        'Ireland': 'Dublin',
        'Israel': 'Jerusalem*',
        'Italy': 'Rome',
        'Jamaica': 'Kingston',
        'Japan': 'Tokyo',
        'Jordan': 'Amman',
        'Kazakhstan': 'Nur-Sultan',
        'Kenya': 'Nairobi',
        'Kiribati': 'Tarawa Atoll',
        'Korea, North': 'Pyongyang',
        'Korea, South': 'Seoul',
        'Kosovo': 'Pristina',
        'Kuwait': 'Kuwait City',
        'Kyrgyzstan': 'Bishkek',
        'Laos': 'Vientiane',
        'Latvia': 'Riga',
        'Lebanon': 'Beirut',
        'Lesotho': 'Maseru',
        'Liberia': 'Monrovia',
        'Libya': 'Tripoli',
        'Liechtenstein': 'Vaduz',
        'Lithuania': 'Vilnius',
        'Luxembourg': 'Luxembourg',
        'Macedonia': 'Skopje',
        'Madagascar': 'Antananarivo',
        'Malawi': 'Lilongwe',
        'Malaysia': 'Kuala Lumpur',
        'Maldives': 'Male',
        'Mali': 'Bamako',
        'Malta': 'Valletta',
        'Marshall Islands': 'Majuro',
        'Mauritania': 'Nouakchott',
        'Mauritius': 'Port Louis',
        'Mexico': 'Mexico City',
        'Moldova': 'Chisinau',
        'Monaco': 'Monaco',
        'Mongolia': 'Ulaanbaatar',
        'Montenegro': 'Podgorica',
        'Morocco': 'Rabat',
        'Mozambique': 'Maputo',
        'Myanmar': 'Rangoon',
        'Namibia': 'Windhoek',
        'Nepal': 'Kathmandu',
        'Netherlands': 'Amsterdam',
        'New Zealand': 'Wellington',
        'Nicaragua': 'Managua',
        'Niger': 'Niamey',
        'Nigeria': 'Abuja',
        'Norway': 'Oslo',
        'Oman': 'Muscat',
        'Pakistan': 'Islamabad',
        'Palau': 'Melekeok',
        'Panama': 'Panama City',
        'Papua New Guinea': 'Port Moresby',
        'Paraguay': 'Asuncion',
        'Peru': 'Lima',
        'Philippines': 'Manila',
        'Poland': 'Warsaw',
        'Portugal': 'Lisbon',
        'Qatar': 'Doha',
        'Romania': 'Bucharest',
        'Russia': 'Moscow',
        'Rwanda': 'Kigali',
        'Saint Kitts and Nevis': 'Basseterre',
        'Saint Lucia': 'Castries',
        'Saint Vincent and the Grenadines': 'Kingstown',
        'Samoa': 'Apia',
        'San Marino': 'San Marino',
        'Sao Tome and Principe': 'Sao Tome',
        'Saudi Arabia': 'Riyadh',
        'Senegal': 'Dakar',
        'Serbia': 'Belgrade',
        'Seychelles': 'Victoria',
        'Sierra Leone': 'Freetown',
        'Singapore': 'Singapore',
        'Slovakia': 'Bratislava',
        'Slovenia': 'Ljubljana',
        'Solomon Islands': 'Honiara',
        'Somalia': 'Mogadishu',
        'South Sudan': 'Juba ',
        'Spain': 'Madrid',
        'Sri Lanka': 'Colombo',
        'Sudan': 'Khartoum',
        'Suriname': 'Paramaribo',
        'Swaziland': 'Mbabane',
        'Sweden': 'Stockholm',
        'Switzerland': 'Bern',
        'Syria': 'Damascus',
        'Taiwan': 'Taipei',
        'Tajikistan': 'Dushanbe',
        'Tanzania': 'Dar es Salaam',
        'Thailand': 'Bangkok',
        'Togo': 'Lome',
        'Trinidad and Tobago': 'Port-of-Spain',
        'Tunisia': 'Tunis',
        'Turkey': 'Ankara',
        'Turkmenistan': 'Ashgabat',
        'Uganda': 'Kampala',
        'Ukraine': 'Kyiv',
        'United Arab Emirates': 'Abu Dhabi',
        'United Kingdom': 'London',
        'United States of America': 'Washington, D.C.',
        'Uruguay': 'Montevideo',
        'Uzbekistan': 'Tashkent',
        'Vanuatu': 'Port-Vila',
        'Vatican City': 'Vatican City',
        'Venezuela': 'Caracas',
        'Vietnam': 'Hanoi',
        'Yemen': 'Sanaa',
        'Zambia': 'Lusaka',
        'Zimbabwe': 'Harare',
    }
