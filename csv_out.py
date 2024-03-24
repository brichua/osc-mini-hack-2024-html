from openai import OpenAI
from ast import Num
from datetime import datetime
from itertools import dropwhile, takewhile
from cleantext import clean
import Org
import instaloader
from itertools import islice

#Make an instaloader object with Braden's account info
L = instaloader.Instaloader()
username = "alexkim440"
password = "Celebration1"
L.login(username, password)

#List of usernames of orgs to fetch data from
targets = ["medi.gators", "ufkickboxing.club", "swamplaunch", "uf_bsu"]
#List of org objects to be created
orgs = []

for user in targets:    
    #Get the profile of the username and all the info
    profile = instaloader.Profile.from_username(L.context, user)
    posts = set(islice(profile.get_posts(), 15))
    bio = profile.biography
    url = profile.external_url
    pfp = profile.profile_pic_url
    name = profile.full_name
    postList = []

    #Set time window
    SINCE = datetime.today()
    UNTIL = datetime(2024, 1, 1)

    #Add all posts from within the time window to postList
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
        postList.append(post)
    
    #Add org object to org list
    org=Org.Org(name, user, pfp, bio, url, postList)
    orgs.append(org)


client = OpenAI()

# context = """Create a Python model using the OpenAI API to process Instagram captions from various student organizations. The model's task is to extract important event information, including the event name, date, time, location, and a brief description, from these captions and output them in a CSV format separated by a semicolon (;).

# Given that these captions often contain details about events hosted by student organizations, it's crucial to prioritize extracting information related to event schedules and locations.

# The model should understand that dates and locations are primary indicators of scheduled events. If a caption contains any of these details, they should be extracted accurately. If a caption lacks specific event information, the model should output 'TBD' (To Be Determined) for the missing fields. If a caption contains multiple events
# or dates, the model should create multiple CSVs with the delimiter,"bRaB", at the end of each set of information EXCEPT for the last event set.

# Limit the number of words for the brief description to 20 words.

# In scenarios where a caption doesn't contain any identifiable event details, it's likely to be more casual or general in nature. In such cases, the model should still output 'TBD' for each field, indicating that no specific event information was found.

# If the caption only contains one piece of useful information (only one value in csv) then output 'TBD' for every field, as having only one piece of information is useless. If you think the output is anything but 5 values separated by semicolons, you are wrong and you should output 'TBD' in every value as an insurance policy.

# The objective is to ensure that the model effectively identifies and extracts event-related information from Instagram captions while handling cases where such information is absent or less prominent.
# """

context = "You will read given text about a club meeting and return, in a csv readable format, the name of event, the date (Month, day as an integer),\
    time with no additional text, location with no additional text, and a brief description of the event strictly in that order.\
        Output event details by separating each value with a semicolon (;).\
          If the text contains something like \"Doors open\
      at 6:00, event starts at 6:30\" you would put 6:30 in the time slot of the csv.\
      If it seems like an appreciation post, a happy birthday post, or anything else that is NOT a meeting announcement, put \"TBD\" in every field\
      If any of these pieces of information are not contained in the text, put \"TBD\" in that respective field.\
      If there is only one value in the csv, simply output 'TBD' in each field.\
      If there are multiple events/dates in one caption, split them up as separate csvs and append the delimiter, 'bRaB', at the end of each."      

post_messages=[{"role": "system", "content": context},
          {"role": "user", "content": "Hello everyone! please come to our meeting on March 23rd at 6pm at Honors Village. Thank you!"},
          {"role": "assistant", "content": "Meeting;March 23;6pm;Honors Village;General meeting."},
          {"role": "user", "content": "Embark on a thrilling journey through Asia at our SASE GBM 4! 🌏\
      Get ready to immerse yourself in a spectacular showcase of cultural games from across the continent.\
      Test your mettle, compete with peers, and may the best team win! 🏆 Join us for an evening filled with fun, laughter, and friendly competition. 🎉\
      If you've signed into at least 2 SASE events this year, you'll receive a FREE exclusive SASE shirt 👕 🤯\
      Don't miss your chance to add this cool merch to your SASE collection ‼️\
      After the games, celebrate your victories or simply unwind with friends at our delightful aftersocial at Koto Hibachi Express & Sushi! \
     🍣🔥 If you need a ride or can offer one, please fill out the carpool form in our Linktree. 🚗💨\
    Date: Tuesday, March 26th\
    Time: doors open 6:00pm, event starts 6:30pm\
    Location: TUR L007"},
          {"role": "assistant", "content": "GBM4;March 26;6:30pm;TUR L007;Asian Cultural showcase with games from across the continent."},
          {"role": "user", "content": "Please join us on April 28th at 5:00pm for our next meeting!"},
          {"role": "assistant", "content": "Meeting;April 28;5:00pm;TBD;General Meeting."},
          {"role": "user", "content": "Hey everyone! I hope you had a nice spring break. Be on the lookout for our next meeting date!"},
          {"role": "assistant", "content": "TBD;TBD;TBD;TBD;TBD"},
          {"role": "user", "content": "It's time... OUR NEXT MEETING. FSA will be having their next meeting on April 1st, at WERT270! Time will be\
           sent out closer to the date. See you all there!"},
           {"role": "assistant", "content": "FSA GBM;April 1;TBD;Wert270;General Body Meeting for FSA"},
           {"role": "user", "content": "Please join us on April 20th at 6:30pm for the best meeting ever. Location to be revealed later!"},
           {"role": "assistant", "content": "Meeting;April 20;6:30pm;TBD;General Meeting."},
           {"role": "user", "content": "🎣 Reel in some compliments with our new exclusive UF SASE shirts! If you've signed into at least 2 SASE events this year, you can grab your very own for FREE at GBM 4! We can't wait to see you there 💚💙"},
           {"role": "assistant", "content": "TBD;TBD;TBD;TBD;TBD"},
           {"role": "user", "content": "Are you ready to tackle SASE's Grand Prix? 🏆 Join us at our third GBM of the semester to learn about the different paths there are after college! 🏎️ You will get to put your racing skills to the test as you navigate through various tracks, including one with a guest racer from @ignite.eii 🏁 Don't forget to take a fun pit stop to hear from our alumni Daniel Shinto and Denise Shinto talk about their post-graduate experiences! 🎓\
            For our first 50 racers, we will be giving out free Kung Fu Tea Boba!🧋 Be sure to be there promptly when doors open 👀\
            As we approach the finish line, make sure to grab a delicious treat at our Jeremiah's Italian Ice Aftersocial. 🍧 Check out the carpool form in our Linktree if you need a ride or can provide one‼️\
            Date: Wednesday, March 6th\
            Doors Open: 6:00pm | Starts: 6:30pm\
            Location: TURL007"},
            {"role": "assistant", "content": "GBM 3;March 6;6:30pm;TURL007;SASE's racing themed GBM discussing all the pathways after college."},
            {"role": "user", "content": "Come to the KUSA x Taekwondo club collab and learn taekwondo to punch and kick away your stress! All levels of experience are welcomed! We're excited to see your cool fight moves🥋 Please make sure to wear comfortable clothes you can work out in and bring water.\
            \
            In order to participate in class, you are required to sign a waiver through Rec Sports. Either through the link in our bio or Rec Sports app, select taekwondo club and follow the procedure to sign the waiver. If you have any issues with signing waivers, please contact our co-President, Olivia, or on the day of the event come few minutes early to have officers to help you with the waivers.\
            \
            If you need a ride to this event, check out our linktree and fill out the carpool form. If you're able to provide rides, please sign up on the form as a driver. Your help would be greatly appreciated :)\
            \
            ★━━━━━━━━━━━━━━━━━━━━★\
            When: March 28th, Thursday\
            Time: 8-10 pm\
            Location: Activity Room 2 in Southwest Rec\
            IN ORDER TO PARTICIPATE, YOU ARE REQUIRED TO SIGN A WAIVER THROUGH REC SPORTS\
            ★━━━━━━━━━━━━━━━━━━━━★"},
            {"role": "assistant", "content": "KUSA x Taekwondo;March28;8-10pm;Activity Room 2 in Southwest Rec;Taekwondo class with members of KUSA ope to all skill levels."},
            {"role": "user", "content": "Blue Origin is a sponsor of UF SASE for the 2023-2024 school year! 🚀 🚀 🚀\
                We met Blue Origin last semester at SASE National Convention and during a Meet & Greet we hosted with FRL! UF SASE looks forward to working with Blue Origin for years in the future. 😄\
                Blue Origin was founded with a vision of millions of people living and working in space for the benefit of Earth. Blue Origin envisions a time when people can tap into the limitless resources of space and enable the movement of damaging industries into space to preserve Earth, humanity's blue origin."},
            {"role": "assistant", "content": "TBD;TBD;TBD;TBD;TBD"},
            {"role": "user", "content": "🎊Happy Birthday Kevin!!!🎊\
                🎉Thank you for all the great work you do as our treasurer! KUSA wishes you a great birthday!🥳"},
            {"role": "assistant", "content": "TBD;TBD;TBD;TBD;TBD"},
            {"role": "user", "content": """UF FSA proudly presents our 2024 Gawad Kalinga Philanthropy Month:

ULAYAW: This year's theme highlights ulayaw, a tagalog word that means close friend or companionship. This year's GK month aims to share the importance of companionship among our community and how we can incorporate this through our philanthropic ventures.

Join us in a month full of fun events as we raise money to help empower impoverished people in the Philippines! All proceeds go to the Gawad Kalinga Foundation

UPCOMING EVENTS:

✨MON, March 18: Blaze Pizza Fundraiser
Location: Blaze Pizza Archer Road
Time: 7 - 10 pm

✨WED - FRI, March 20 - 22: Pie-milya
Location: Turlington Plaza
Time: 11 am - 2 pm

✨SUN, March 24: Jeremiah's Fundraiser
Location: Jeremiah's Italian Ice Butler Plaza
Time: 12 - 6 pm

✨FRI, April 5: Basketball Tournament
Location: TBA
Time: TBA

stay tuned for more information and events!"""},
{"role": "assistant", "content": "Blaze Pizza Fundraiser;March 18;7-10pm;Blaze Pizza, Archer Road;Fundraiser at Blaze Pizza, partial proceeds towards UF FSA.bRaB\
 Pie-milya;March 20;11am-2pm;Turlington Plaza;Pie the members of FSA Board!bRaB\
 Basketball Tournament;April 5;TBA;TBA;Come out and play basketball!"},
 {"role": "user", "content": "With the Spring Undergraduate Research Symposium just around the corner, Apr. 1, join us for our Symposium 101 Workshop. Learn the do’s and dont’s of presenting research!"},
{"role": "assistant", "content": "Symposium 101 Workshop;April 1;TBD;TBD;Workshop to better your understanding and practice of research."}
 ]
bio_messages=[{"role": "system", "content": "Create a Python prompt for the OpenAI API to analyze Instagram bios of student organizations and generate identifying tags based on their focus or theme. For instance, input bios from engineering organizations should output engineering-related tags, while bios from cultural organizations should yield cultural tags. Design teams' bios should prompt the model to output design-related tags. The prompt should be designed to accurately identify and categorize student organizations based on their bios. These tags will be separated with semicolons and EXACTLY 3 tags should be generated.\
               The tags are STRICTLY LIMITED to the following: Stem, Engineering, Cultural, Social, Leadership, Professional, Medical, Design, Sports, Competitive, Art, Creative, Service, Inclusion, and Community"},
              {"role": "user", "content": """🧪 | Society of Asian Scientists and Engineers (SASE) at the University of Florida
⚙️ | Follow us and join our Discord for updates!
@ufsasesports"""},
                {"role": "assistant", "content": "Cultural;Engineering;STEM" },
                {"role": "user", "content": "University of Florida’s student-run organization dedicated to building a solar race car.\
🥇- FSGP '23"},
                {"role": "assistant", "content": "Design;Engineering;Stem"},
                {"role": "user", "content": """University of Florida 🐊 Established in 1985
Korean Undergraduate Student Association 🇰🇷❤︎
KUSA Dance: @ufkusadance
KUSA Sports: @ufkusasports"""},
                {"role": "assistant", "content": "Cultural;Social;Casual"},
                {"role": "user", "content": """The Freshman Leadership Engineering Group is a professional and selective student organization within UF's College of Engineering."""},
                {"role": "assistant", "content": "Professional, Engineering, Leadership"},
                {"role": "user", "content": """DTE is composed of students who design technologies to improve patient experiences at Shands Children's Hospital. Partnered with @ufdreamteam"""},
                {"role": "assistant", "content": "Medical, Engineering, STEM"},
                {"role": "user", "content": """🐊 #GoGators 🏐
@ecva_vball
Division I🥇| ‘20
Division I🥈| ‘97, ‘10
Division I🥉| ‘18
Conference🥇| ‘18
Southeast🥇| ‘17, ‘18, ‘19, ‘20
@thencvf"""},
                {"role": "assistant", "content": "Sports, Competitive, Athletics"},
                {"role": "user", "content": """Health Educated Asian Leaders
• University of Florida
• Pre-Health. Service. Leadership. Ohana.
Important Links for HEAL:"""},
                {"role": "assistant", "content": "Medical, Cultural, Leadership"},
                {"role": "user", "content": """The Premier Aerospace Design Team at the University of Florida @uflorida."""},
                {"role": "assistant", "content": "Design, STEM, Engineering"},
                {"role": "user", "content": """FLP strives to cultivate creativity, community, and leadership, through various networking, team-building, and service opportunities."""},
                {"role": "assistant", "content": "Leadership, Professional, Service"}
                    ]

def main():
        csv_file = open("org_events.txt", "w")
        for org in orgs:
             process_bio_input(org.bio)
             events = []
             org_photos = []
             realname = org.realname
             realname = clean(realname, no_emoji=True)
             csv_file.write(realname + " n4mE ")
             pfp = org.pfp
             csv_file.write(pfp)
             csv_file.write(" P4p ")
             bio = org.bio
             bio = clean(bio, no_emoji=True)
             csv_file.write(bio)
             csv_file.write(" b10 ")
             tags = process_bio_input(bio)
             csv_file.write(tags)
             csv_file.write(" t4Gs ")
             
             if len(org.posts) == 0:
                 csv_file.write("bRaB")
             else:
                for post in org.posts:
                    caption = post.caption
                    csv = process_post_input(caption, events)
                    if csv != "TBD;TBD;TBD;TBD;TBD":
                        csv = clean(csv, no_emoji=True)
                        csv_file.write(csv +"bRaB")

                    if csv == "TBD;TBD;TBD;TBD;TBD":
                        if post.typename == "GraphSidecar":
                            for slide in post.get_sidecar_nodes():
                                if slide.is_video == False:
                                    org_photos.append(slide.display_url)
                        if post.is_video == False:
                            org_photos.append(post.url)

             csv_file.write(" 3vEnt5 ")
             for photo in org_photos:
                 csv_file.write(photo + " ")
             csv_file.write(" 9nD ")
        csv_file.close()

def converse_with_chatGPT(events):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=post_messages)
    message = completion.choices[0].message.content
    if message in events:
        return "TBD;TBD;TBD;TBD;TBD"
    else:
        events.append(message)
        return message

def process_post_input(post, events):
    user_post = (f"{post}")
    add_message("user", user_post)
    result = converse_with_chatGPT(events)
    print(result)
    return result

def add_message(role, message):
    post_messages.append({"role": role, "content": message})

def process_bio_input(bio):
    bio_input = (f"{bio}")
    bio_messages.append({"role": "user", "content": bio_input})
    result = bio_analysis()
    return result

def bio_analysis():
    tag_generator = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=bio_messages)
    tags = tag_generator.choices[0].message.content
    bio_messages.append({"role": "assistant", "content": tags})
    return tags

main()
