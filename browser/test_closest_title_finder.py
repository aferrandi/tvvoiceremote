from unittest import TestCase

from browser.closest_title_finder import PossibleMatch, ClosestTitleFinder


class TestClosestTitleFinder(TestCase):
    def test_fuzzy_search_of_text(self):
        titles = [
            'The Night Agent',
            'Castlevania: Nocturne',
            'Stargate SG-1',
            'Badland Hunters',
            'Mr. Mercedes',
            'Dexter',
            'Agente 007 – Missione Goldfinger',
            'Agente 007 - Una cascata di diamanti',
            '007 - Bersaglio mobile',
            'Agente 007 - Vivi e lascia morire',
            'Agente 007 - Al servizio segreto di sua maestà',
            'Prometheus',
            'Animal Kingdom',
            'Homeland',
            'The Beast in Me',
            'The Walking Dead',
            'Dark Winds',
            'Il problema dei 3 corpi',
            'No Time to Die',
            'Priest',
            'Hanna',
            'La Torre Nera',
            'Jack Reacher: Punto di non ritorno',
            'Kill Bill: Vol. 2',
            'Blood of Zeus',
            'BLUE EYE SAMURAI',
            'Neon Genesis Evangelion',
            'Abigail',
            'Devil May Cry',
            'Intervista col vampiro',
            'The Swedish Connection',
            'La famiglia Addams',
            'La famiglia Addams 2',
            'The Rip - Soldi sporchi',
            'Prometheus',
            'Kung Fu Panda 3',
            'Bones',
            'Deadwind',
            'Fargo',
            'Dept. Q - Sezione casi irrisolti',
            'Altered Carbon',
            'Avvocato di difesa - The Lincoln Lawyer',
            'Lost in Space',
            'October Faction',
            'The Recruit',
            'La Brea',
            'Another Life',
            'Outer Banks'
        ]
        possible_matches = [PossibleMatch[None](None, t) for t in titles]
        self.assertEqual("Agente 007 – Missione Goldfinger", self.movie_box_with_text(possible_matches, "Goldfinger"))
        self.assertEqual("Agente 007 – Missione Goldfinger", self.movie_box_with_text(possible_matches,  "Goldhinger"))
        self.assertEqual("Avvocato di difesa - The Lincoln Lawyer", self.movie_box_with_text(possible_matches,  "Lincoln"))
        self.assertEqual("Il problema dei 3 corpi", self.movie_box_with_text(possible_matches,  "corpe"))
        self.assertEqual("La famiglia Addams", self.movie_box_with_text(possible_matches,  "addams"))
        self.assertEqual("No Time to Die", self.movie_box_with_text(possible_matches, "time die"))
        self.assertEqual("Agente 007 – Missione Goldfinger", self.movie_box_with_text(possible_matches, "Agente Missione"))

    def movie_box_with_text(self, possible_matches: list[PossibleMatch[None]], text_to_find: str) -> str:
        return ClosestTitleFinder.fuzzy_search_of_text(possible_matches, text_to_find).possible_match.text
