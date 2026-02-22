from unittest import TestCase

from browser.closest_title_finder import PossibleMatch, ClosestTitleFinder


class TestClosestTitleFinder(TestCase):
    """
    <a href="/browse/original-audio" data-navigation-tab-name="audioSubtitles">Sfoglia per lingua</a>
    """

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
        self.assertEqual("Agente 007 – Missione Goldfinger", ClosestTitleFinder.fuzzy_search_of_text(possible_matches, "Goldfinger").possible_match.text)

