import json
import requests
from typing import List, Dict


class MilliPiyango:

    ERROR_MSGS = {
        "CODE-01": "Geçersiz Parametre: 'oyun_adi'. 'oyun_adi' parametresi olarak yalnızca {} gönderilebilir.",
        "CODE-02": "Geçersiz Parametre: 'tarih'. 'tarih' parametresi olarak gönderebileceğiniz tarihleri kontrol ediniz.",
        "CODE-03": "Servis Hatası: Milli Piyango sitesinden veri getirilirken bir hata oluştu. Daha sonra tekrar "
                   "deneyiniz.",
        "CODE-04": "Geçersiz İstek: Lütfen gönderdiğiniz parametreleri kontrol ediniz. \n1) 'oyun_adi' parametresi "
                   "olarak yalnızca {} gönderilebilir. \n2) 'tarih' parametresi olarak gönderebileceğiniz tarihleri "
                   "kontrol ediniz.",
        "CODE-05": "Geçersiz Parametre: 'biletNo'. 'biletNo' parametresi 6 karakterli bir sayı olmalıdır."
    }

    PIYANGO = "piyango"
    SAYISAL = "sayisal"
    SANS_TOPU = "sanstopu"
    ON_NUMARA = "onnumara"
    SUPER_LOTO = "superloto"

    GAME_LIST = [PIYANGO, SAYISAL, SANS_TOPU, ON_NUMARA, SUPER_LOTO]

    URL_FOR_DRAW_DATES = "http://www.millipiyango.gov.tr/sonuclar/listCekilisleriTarihleri.php?tur={}"
    URL_FOR_RESULTS = "http://www.mpi.gov.tr/sonuclar/cekilisler/{}/{}.json"

    @staticmethod
    def process_response(resp, error_message: str) -> dict:
        if resp.ok and resp.status_code == 200:
            try:
                data = resp.json()
            except json.decoder.JSONDecodeError as jsDecodeError:
                # TODO: add proper exception handling
                data = resp.content.decode("utf-8-sig").encode("utf-8")
                data = json.loads(data)
            return data
        else:
            return {
                'error': error_message,
                'response': {
                    'code': resp.status_code,
                    'url': resp.url
                }
            }

    def get_draw_dates(self, game: str) -> dict:
        if game not in self.GAME_LIST:
            return {
                'error': self.ERROR_MSGS['CODE-01'].format(", ".join(self.GAME_LIST)),
                'request': {'oyun_adi': game}
            }

        response = requests.get(self.URL_FOR_DRAW_DATES.format(game))

        return self.process_response(response, self.ERROR_MSGS['CODE-03'])

    def get_result(self, game: str, date: str) -> dict:
        if game not in self.GAME_LIST:
            return {
                'error': self.ERROR_MSGS['CODE-01'].format(", ".join(self.GAME_LIST)),
                'request': {'oyun_adi': game}
            }

        available_dates: List[Dict] = self.get_draw_dates(game)
        available_dates: List[str] = [d['tarih'] for d in available_dates]
        if date not in available_dates:
            return {
                'error': self.ERROR_MSGS['CODE-02'],
                'request': {'tarih': date}
            }

        response = requests.get(self.URL_FOR_RESULTS.format(game, date))

        return self.process_response(response, self.ERROR_MSGS['CODE-04'].format(", ".join(self.GAME_LIST)))

    def get_result_for_piyango(self, date: str, ticket_no: str) -> dict:
        available_dates: List[Dict] = self.get_draw_dates(self.PIYANGO)
        available_dates: List[str] = [d['tarih'] for d in available_dates]
        if date not in available_dates:
            return {
                'error': self.ERROR_MSGS['CODE-02'],
                'request': {'tarih': date}
            }

        if len(ticket_no) != 6:
            return {
                'error': self.ERROR_MSGS['CODE-05'],
                'request': {'biletNo': ticket_no}
            }

        result_for_piyango = self.get_result(self.PIYANGO, date)
        for res in result_for_piyango['sonuclar']:
            number_for_comparison = (
                ticket_no[len(ticket_no) - res['haneSayisi']:len(ticket_no)] if res['tip'] != 'TESELLI'
                else ticket_no
            )
            for number in res['numaralar']:
                if number == number_for_comparison:
                    result = {
                        'kazandi': True,
                        'tip': res['tip'],
                        'ikramiye': res['ikramiye'],
                        'kacBildi': res['haneSayisi'] if res['tip'] != 'TESELLI' else 6,
                        'numara': number,
                        'biletNo': ticket_no
                    }
                    return result
        return {'kazandi': False, 'biletNo': ticket_no}

    def run_sample(self) -> None:
        res = self.get_draw_dates(self.ON_NUMARA)
        print(res)
        res = self.get_result(self.ON_NUMARA, res[-1]['tarih'])
        print(res)
        #  TODO: add sample result for piyango result 1 for winner 1 for loser
