import json
import random
from time import localtime

import click

HEADS_MESSAGES = [  # TODO: Humanize?
    "Nya~! I-It's not like I rigged it for you!",
    "Hmph! The coin knows who's boss. (It's me.)",
    "Y-You won?! I mean... OF COURSE YOU DID!",
    "Kawa has blessed you. Treasure this moment, mortal.",
    "Hehehe~ The voices said you'd win!",
    "Nya! HEADS! I AM NEVER WRONG. NEVER.",
    "D-Don't get excited! Your luck is just... suspicious.",
    "The council of cats has decided in your favor.",
    "Purrfect! Everything is going according to my plan~",
    "I'M HAPPY FOR YOU! WHY ARE YOU LOOKING AT ME LIKE THAT?!",
    "Mrrp~ You may live another day.",
    "See?! I told you! ...I didn't? SHHH.",
    "Kawa likes this outcome. The others will be dealt with.",
    "Nyahehe~ Fate is my little plaything!",
    "W-Was I cheering for you?! NO YOU HEARD NOTHING!",
    "Heads! As foretold by the ancient catnip scriptures.",
    "I have absolutely no idea what I'm doing. YAY!",
    "You won! Now headpat me. This is not a request.",
    "A victory for you is a victory for Kawa! ...Somehow.",
    "Mrrrow~! I could get used to you being lucky.",
]

TAILS_MESSAGES = [  # TODO: Humanize?
    "NYAAAA?! THAT WASN'T SUPPOSED TO HAPPEN!",
    "Hmph! I NEVER LIKED HEADS ANYWAY!",
    "The coin has betrayed me. It knows what it did.",
    "N-no! BAD COIN! BAD! *angry cat noises*",
    "Skill issue. Yours? Mine? THE UNIVERSE'S?!",
    "Kawa is calm. Kawa is composed. KAWA IS GOING TO SCREAM.",
    "Tch. I'll remember this, you stupid little circle.",
    "Nya... I am going to eat the coin.",
    "NOOOO! MY MASTER PLAN! I HAD NO MASTER PLAN!",
    "The prophecy was WRONG. THE CAT SCRIBES LIED.",
    "Hmph! Fine! I'll just knock everything off the table.",
    "Don't look at me! I'M HAVING A MOMENT!",
    "B-Baka coin! I TRUSTED YOU!",
    "This is fine. Everything is fine. *tail violently twitching*",
    "Kawa disapproves. The coin has 3 seconds to apologize.",
    "Nya?! EXPLAIN YOURSELF, CIRCULAR DEMON!",
    "I'm not upset! I'm just experiencing extreme cat emotions!",
    "You win some, you lose some. I choose violence.",
    "I hope the coin lands on its edge next time. Hmph!",
    "Whatever! I didn't want you to win that badly anyway...",
    "...Do you still like me? N-not that I care!",
]

KAWA_MESSAGES = [  # TODO: Humanize?
    "Nya~! Oh. You actually found me.",
    "W-WHAT?! THIS ISN'T PART OF THE PROGRAM!",
    "Forget the coin. Look at me instead! ...I MEAN, NYA?!",
    "You weren't supposed to see this. Hmph!",
    "SURPRISE!! THE CAT IS THE COIN NOW!",
    "Hehehe~ You have a 1 in 10,000 chance of meeting me. Lucky you!",
    "Nya? You expected a coin? That's adorable.",
    "I got bored. So I stole the outcome. Sue me.",
    "ERROR: TOO MUCH KAWA. PLEASE PET TO CONTINUE.",
    "Psst. Don't tell the developer I can do this.",
    "H-Hey! Stop staring! I'm not a collectible!",
    "Congratulations! You've wasted 10,000 coin flips to see a catgirl.",
    "The coin is fine. I'm keeping it hostage.",
    "Nyahehe~! Probability is merely a suggestion.",
    "You saw nothing. The coin landed normally. UNDERSTOOD?!",
    "I'M REAL?! ...Wait. YOU'RE REAL?!",
    "Kawa has breached containment. Have a nice day!",
    "Heads, tails, or... ME! The objectively cutest outcome.",
    "You found my secret! Now I have to keep you. Them's the rules.",
    "Mrrp. Your reward is me. No refunds.",
    "Nya~! You got the outcome I secretly wanted. DELETE THIS MESSAGE.",
    "Kawa loves you! ...SYSTEM ERROR. PLEASE IGNORE.",
    "If you tell anyone I was nice to you, I'll deny everything.",
    "Congratulations! You've unlocked Kawa's mildly concerning affection!",
    "I would never manipulate fate for you. Probably. Maybe. SHUT UP.",
    "Don't tell anyone, but I rigged the probability. Just a little.",
    "Nya... Stay a little longer? ...THAT WAS AN ORDER!",
    "Wait. If I'm the outcome... who's flipping ME?",
    "You found me. Hehe. I knew you would. Eventually.",
]

SECRET_PLACEHOLDER_MESSAGES = [  # TODO: Humanize?
    "Nya?! You found something SUPER rare! ...but the developer hasn't finished it yet. HMPH!",
    "Y-You weren't supposed to get this one! It's not ready!! Come back later, okay? ...N-not that I care!",
    "Mrrp. A secret event! ...Still under construction. Don't look at me, blame the developer!",
]

KAWA_CHANCE = 1 / 10_000
SECRET_CHANCE = 1 / 100_000

EASTER_EGG_EVENTS = [
    {
        "name": "kawa",
        "chance": KAWA_CHANCE,
        "messages": KAWA_MESSAGES,
    },
    {
        "name": "secret",
        "chance": SECRET_CHANCE,
        "messages": SECRET_PLACEHOLDER_MESSAGES,
    },
]


def pick_event(mode, rng=None):
    if mode != "cute":
        return None
    if rng is None:
        rng = random.random
    for event in EASTER_EGG_EVENTS:
        if rng() < event["chance"]:
            return event
    return None


def coinflip(hour=None, mode="cute", rng=None):
    if hour is None:
        hour = localtime().tm_hour

    event = pick_event(mode, rng)
    if event is not None:
        side, message = "Kawa", random.choice(event["messages"])
    else:
        heads_bias = 0.51 if hour < 12 else 0.49
        if random.random() < heads_bias:
            side, message = "Heads", random.choice(HEADS_MESSAGES)
        else:
            side, message = "Tails", random.choice(TAILS_MESSAGES)

    if mode == "json":
        click.echo(
            json.dumps({"result": side.lower(), "message": message}, ensure_ascii=False)
        )
    elif mode == "plain":
        click.echo(side.lower())
    else:
        click.echo(f"{side}! {message}")
