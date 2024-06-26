example_text0 = 'Black Holes tests (Test2) test3. test4, test5; test5, ' \
                'test4 so is the black holes'

example_text1 = "Black holes are some of the strangest and most fascinating " \
               "objects in space. They're extremely dense, with such strong " \
               "gravitational attraction that not even light can escape " \
               "their grasp. The Milky Way could contain over 100 million " \
               "black holes, though detecting these gluttonous beasts is " \
               "very difficult."

example_text2 = "Online reinforcement learning (RL) is increasingly popular " \
                "for the personalized mobile health (mHealth) intervention. " \
                "It is able to personalize the type and dose of " \
                "interventions according to user’s ongoing statuses and " \
                "changing needs. However, at the beginning of online " \
                "learning, there are usually too few samples to support the " \
                "RL updating, which leads to poor performances. A delay in" \
                " good performance of the online learning algorithms can be" \
                " especially detrimental in the mHealth, where users tend to " \
                "quickly disengage with the mHealth app. To address this " \
                "problem, we propose a new online RL methodology that " \
                "focuses on an effective warm start. The main idea is to " \
                "make full use of the data accumulated and the decision rule " \
                "achieved in a former study. As a result, we can greatly " \
                "enrich the data size at the beginning of online learning in " \
                "our method. Such case accelerates the online learning " \
                "process for new users to achieve good performances not only " \
                "at the beginning of online learning but also through the " \
                "whole online learning process. Besides, we use the decision " \
                "rules achieved in a previous study to initialize the " \
                "parameter in our online RL model for new users. It " \
                "provides a good initialization for the proposed online " \
                "RL algorithm. Experiment results show that promising " \
                "improvements have been achieved by our method compared " \
                "with the state-of-the-art method."

ctext = example_text0
from zb_msc_classificator.config.definition import ConfigEntityLinking
from zb_msc_classificator.entity_linking import EntityLink

el = EntityLink(
    config=ConfigEntityLinking()
)
t1 = el.execute(ctext)

print(t1)


