# semiengineering_com - minimum-energy-per-query

**来源**：https://semiengineering.com/minimum-energy-per-query/
**日期**：20260311

---

Submit
Subscribe
Home
Systems & Design
Low Power - High Performance
Manufacturing, Packaging & Materials
Test, Measurement & Analytics
Auto, Security & Enabling Technologies
Special Reports
Business & Startups
Jobs
Knowledge Center
Technical Papers
Home
';
AI/ML/DL
Architectures
Automotive/ Aerospace
Communication/Data Movement
Design & Verification
Lithography
Manufacturing
Materials
Memory
Optoelectronics / Photonics
Packaging
Power & Performance
Quantum
Security
Test, Measurement, Analytics tech papers
Transistors
Z-End Applications
Events & Webinars
Events
Webinars
Videos & Research
Videos
Industry Research
Newsletters & Store
Newsletters
Store
MENU
Home
Special Reports
Systems & Design
Low Power-High Performance
Manufacturing, Packaging & Materials
Test, Measurement & Analytics
Auto, Security & Enabling Technologies
Knowledge Center
Videos
Startup Corner
Business & Startups
Jobs
Technical Papers
Events
Webinars
Industry Research
Newsletters
Store
Special Reports
Home
>
Low Power-High Performance
>
                                                                Minimum Energy Per Query
Low Power-High Performance
Minimum Energy Per Query
How much of the energy consumed in an AI chip is spent doing something useful? This question affects everything from software to system architecture to chip design.
February 12th, 2026 - 

								By:
Brian Bailey
Key Takeaways
Extracting heat from a chip faster is a short-term fix to a bigger problem.
The longer-term challenge is how to reduce the amount of energy used per query.
Data movement, guardbanding, and software inefficiency are key targets for the future.
Heat is a serious problem within AI chips, and it is limiting how much processing can be done. The solution is either to extract heat faster, or generate less of it. Neither approach is easy, but long-term solutions need to focus on the second option.
Every action within a chip consumes energy and generates heat, which must be removed from the chip. The amount of activity is limited by the amount of heat that can be removed and the speed at which that happens. Many advances are being made to reduce energy consumption, and while possible, they are expensive and
consume additional energy
.
But that’s only part of the problem. The total amount of available energy is not fully elastic, and increases in energy production are not keeping up with rising demand for incremental energy.  And this begs the question, ‘Is all of the activity useful, and is it being done using the minimum amount of energy possible?’ Given that the human brain consumes about 20 watts, there is clearly a lot of potential for future optimization, but all advances must make economic sense.
It is often said that to understand something, you have to follow the money. That may be very important here, because power consumption is no longer just inconvenient. It is now a major cost factor. “While power has risen in importance, it has always been considered a second-class citizen in chip design,” says Marc Swinnen, director of product marketing at
Synopsys
. “But it leads directly to the bottom line, and the cost of cooling is quite intense. You pay for the electricity to heat up the circuits when you run them, and pay again for more electricity to pump the heat out. Power has become a significant contributor to the cost of the system.”
That is why incremental improvements in heat extraction are the favored solution so far. “While power is important, and it’s good to know how much energy your algorithm will consume, it is not the first design criterion,” says Roland Jancke, head of department design methodology at
Fraunhofer IIS’
Engineering of Adaptive Systems Division. “It does play a more important role at the system level, but you do not have enough information about power consumption of your algorithm or your component. There are so many possibilities, many of which will never even be part of the investigation. Performing architectural studies is difficult.”
Work is underway at large systems companies to address this, but it is being kept quiet for competitive reasons. “Some of this work is so new that they feel they have the edge because they started to pay attention to it a little bit earlier than others,” says Suhail Saif, director of product management and solutions engineering at
Keysight EDA
. “It’s all secretive and in-house, where every design house doesn’t know where the competition is. They feel they have an edge, and it is their moat. They want to keep it close to their chest for the moment. It will need more maturity in the industry before they decide it is not worth it, when everyone is doing almost the same thing and there’s no return on investment. Then they will let one of the EDA companies handle it. And while everybody will then benefit from it, it’s less effort, less headache. I don’t think we are there yet.”
Consider communications
For the past several decades, the industry has sought improvement through aggregation. More and more content was integrated into a single monolithic die, and for the most part this defined the size of the compute problem that was tackled for standard applications. That stopped being the case with AI, where massive arrays of processors, spread across racks and even data centers, became part of the mainstream.
“A lot of the power is consumed by communication between chips,” says Synopsys’ Swinnen. “Part of the penalty of disaggregation is that you have more communication costs between the blocks in your system. One of the beauties of monolithic was that the communication was low-power and high-bandwidth. Data centers are another form of disaggregation. We have multiple processors across multiple racks, many yards away from each other. They’ve looked at the communication power, and that can be reduced by going optical. The data backplane in the data centers is becoming optical.”
All aspects of communications are being investigated. “Take a look at the recent industry efforts for high-performance communication protocols,” says Badarinath Kommandur, fellow at
Cadence
. “There is a pretty intense focus on metrics like picojoules per bit. Moving forward, the industry wants to get to femtojoules per bit. This is becoming front and center, especially in AI-driven applications.”
Compute fabrics are becoming so performance-intensive that traditional communications is struggling to keep up. “Copper has been the focus for a long time, but if you look at it in terms of speed scaling, we are now contending with skin effect, which impacts how electrons flow through the medium,” says David Kuo, vice president for product marketing and business development at Point2 Technology. “There’s a limit for how copper can support the future data center workloads. With optical, there’s cost, power, and reliability issues. There’s a saying in the data center, use copper when you can, use optical when you have to.”
There is great reluctance to make that switch. “Optics is a step function in complexity,” says Swinnen. “There is a new set of physics, and a different set of tool expertise required. Then there are issues marrying optics and semiconductors together. It’s gotten a lot better. While people talk a lot about picojoules per bit, photonic systems are much more efficient in that they require less energy per bit to transmit the data. But that number is low because they have such high bandwidth, not because they’re low power.”
Point2 Technology is looking at a possible middle ground. “We have developed an eTube technology,” says Kuo. “It uses RF transmission to transmit data over a plastic waveguide. We are replacing the copper medium with a plastic material, and we define the waveguide structure. Then, using an RF transmitter and receiver, we transfer the signal over the waveguides. The antenna is very similar to patch antennas.”
On-chip communications also must be considered. “For modern multi-core and multi-die SoCs, moving data around — weights, activations, and metadata — costs far more energy than the compute that processes it,” says Guillaume Boillet, vice president of strategic marketing at
Arteris
. “This shifts the network-on-chip (NoC) from being an integration fabric to being one of the primary levers for power optimization. Teams that architect their NoC around workload traffic patterns can dramatically reduce data movement, localize communication, minimize congestion, and cut dynamic power across the chip. In a world increasingly limited by watts, controlling where data flows and how efficiently it moves is becoming just as important as optimizing the compute itself.”
Consider design
While many AI workloads are somewhat general-purpose, inference applications can often be tuned to directly address immediate needs. “We have to come up with hardware architectures that exploit the network architecture itself,” says Sharad Chole, chief scientist at
Expedera
. “Edge devices are basically limited by bandwidth. Training is done using multiple HBMs. But on the edge, there is literally one LPDDR, or not even 64 channels, maybe even a smaller-channel LPDDR that gets deployed on low-cost edge devices. That means bandwidth management becomes a critical part of how we execute things on edge inference.”
Most of today’s wasted power does not come from the arithmetic itself, but from everything around it. “Unnecessary data movement, poorly matched memory hierarchies, unused speculative work, glitch power, and guardbands that assume worst-case conditions that rarely occur are just a few examples of waste,” says Arteris’ Boillet. “Meaningful improvement must therefore come from electronic productivity — maximizing useful work per Joule — throughout the entire stack, from system scheduling and workload shaping to architectural and micro-architectural efficiency. In a world increasingly limited by watts, controlling where data flows and how efficiently it moves is becoming just as important as optimizing the compute itself.”
Consider implementation
While there may be large gains to be made at the architectural level, significant waste also may persist through implementation. “Fixed-voltage guardbands were meant to provide safety, but over time they have become an energy tax baked into every chip,” says Noam Brousard, vice president of solutions engineering at
proteanTecs
. “Guardbands assume that every worst case will happen at the same time. In reality, that almost never occurs. Yet the chip is forced to run at an inflated voltage all the time. The result is obvious. The chip burns energy it does not need to use. This unused margin translates into gigawatts of waste. It is a hidden cost that grows with every generation.”
Guardbands are also created to deal with uncertainty. “The PDK comes from the foundry processes,” says Kuo. “But is it accurate enough to describe transistor-level performance? What we find is it is not quite accurate enough. You get a surprise when you get to silicon. With analog and RF design, the reason it is so challenging is that you’re constantly pushing the boundaries beyond what the foundry can actually define.”
AI designs certainly push process boundaries. “For the more advanced PDKs, any leading foundry will take the silicon learnings and optimize them for the designs they’re targeting in high volume,” says Cadence’s Kommandur. “It is quite possible that if you’re designing something first time around with the 0.5 PDK, or something close to that, your end high-volume manufacturing silicon PDKs will be quite different. You really have to adapt to the evolution of PDKs for these advanced nodes. For mature nodes, where the silicon to PDK correlation is extremely high, you are optimizing design based on what you expect to see in silicon. The foundry certainly puts in some pessimism.”
Some techniques can adapt to this level of uncertainty. “Traditional approaches like DVFS and AVS cannot solve this,” says proteanTecs’ Brousard. “They rely on limited visibility and indirect estimates, so they still require large guard bands. While these are good indications of the stress a specific workload applies, it is a second-order indication. Without direct insight into real path delays, you cannot safely remove margin. You cannot optimize what you cannot see.”
Brousard says that real-time silicon feedback systems are required to get rid of the guard bands. “We achieve this by utilizing small-footprint IP integrated across the chip that continuously monitors the margin to timing failure of millions of real logic paths in mission mode,” he explains. Since the timing margin itself is the ultimate indicator of performance health, monitoring it directly makes the system agnostic to the individual factors causing degradation (be it workload, temperature, aging, or voltage droops). They measure in real time for each P-state, for each functional workload running on a specific P-state, and even throughout each workload.”
Another form of wasted power that performs no useful function is glitches. “This has long been neglected,” says Swinnen. “And it is a significant portion of total power. It is difficult to analyze because it depends on precise timing. Only recently have tools existed that are able to analyze this and reduce it.”
While AI created some of these problems, it also can help solve them. “Optimizing PPA using AI is extremely challenging,” says William Wang, CEO of
ChipAgents
. “You are tackling major issues like balancing power and area tradeoffs and avoiding reward hacking, but it’s also incredibly promising. Human engineers can only juggle a limited number of factors in power-sensitive design, whereas AI can reason across a much broader context and surface design recommendations that deliver real efficiency gains early in the stack.”
Consider software
Designers may be looking to eke out every power improvement they can, but it can all be for nothing if software asks hardware to perform unnecessary work. “The semiconductor industry is responsible for power consumption and the power envelope, meeting power targets,” says Keysight’s Saif. “But software also needs to think about this. Software is the master in system design, but hardware is the execution engine for the commands that come from software. Software might not be paying as much attention to this pain point as they need to.”
There has to be some degree of hardware/software co-design. “Improving power efficiency is a complicated system hardware and software challenge,” says Steven Woo, fellow and distinguished inventor at
Rambus
. “To achieve the best application performance and power efficiency, hardware must provide the right acceleration features, and software must be designed to use these features to their fullest capabilities. This can mean re-designing algorithms, refactoring software, and having applications developers be more architecturally aware of system hardware characteristics like cache sizes, DRAM, and storage tiers. Data movement continues to be a major consumer of power, and applications developers need to be aware of potential tradeoffs in storing and retrieving intermediate results versus simply recomputing these results if power can be saved.”
For many years, chipmakers have been asking for software productivity improvements. “If you look back 20 years, a lot of software was programmed using low-level programming languages,” says Andy Heinig, department head for efficient electronics at Fraunhofer IIS’ Engineering of Adaptive Systems Division. “That was time-consuming and painful, but with each level of abstraction we also lose power efficiency. If you look at how software is designed, it’s not very efficient, and we lose a lot of power. It makes it easier to program software. But a lot of efficiency is gone by this type of programming.”
There is little hardware can do to overcome bad software. “Hardware is optimizing the way it executes software commands, but software needs to be more aware of what commands are sent to hardware,” says Saif. “They need to be aware of the downstream challenge of managing the power envelope, keeping within budget. I interact with enough hardware engineers to know their frustration with the software processes.”
Conclusion
There appears to be general agreement within the industry that data movement is expensive, both in terms of performance and power consumption. The only acceptable answer, in the long term, is how to significantly reduce the need for it. But today, the solutions being created are how to optimize the power consumed by it. While this is a predictable strategy for the semiconductor industry, it allows for a major disruption in coming years when someone solves the real problem —  and that will involve software.
Tags:
AI
Arteris
Cadence
ChipAgents
Expedera
Fraunhofer IIS EAS
GuardBands
Keysight EDA
low power
optical
PDK
Point2 Technology
power efficiency
proteanTecs
Rambus
software
Synopsys
Brian Bailey
(all posts)
Brian Bailey is Technology Editor/EDA for Semiconductor Engineering.
1 comments
Ashfaq
says:
February 21, 2026 at 1:42 am
first read on the website. enjoyed the flow of the post.
Reply
Leave a Reply
Cancel reply
Comment
*
Name
*
(Note: This name will be displayed publicly)
Email
*
(This will not be displayed publicly)
Δ
Technical Papers
FeFETs With Laminated Gate Stacks For Radiation Resilience in Vertical NAND (Georgia Tech)
March 10, 2026
by Technical Paper Link
Wafer-on-Wafer Hybrid Bonding: Reticle Placements To Achieve Efficient NW Topologies (ETH Zurich)
March 9, 2026
by Technical Paper Link
A Framework That Generates Chip Layouts Directly From Natural Language Specifications (U. of Bristol, RAL)
March 9, 2026
by Technical Paper Link
Unified, Traceable Framework For Risk Assessment in Automotive Semiconductors (Robert Bosch)
March 9, 2026
by Technical Paper Link
10-Year Roadmap for AI + Hardware (UIUC, UCLA, Stanford et al.)
March 6, 2026
by Technical Paper Link
Knowledge Centers
Entities, people and technologies explored
Learn More
Related Articles
Liquid Cooling Gains Traction In Data Centers
There are numerous ways to remove heat from chips, and more are on the way.
by
Bryon Moyer
Chiplets Vs. Soft IP: Different In Almost Every Way
A chiplet marketplace would require deep changes in the design-through-manufacturing flow.
by
Bryon Moyer
Multiple AI Scale-Up Options Emerge
As data center infrastructures adapt to evolving workloads, parts of Ethernet can be found in scale-up approaches.
by
Bryon Moyer
Will 2026 Be Dominated By AI?
Artificial intelligence has become central to almost all advances happening within semiconductors and EDA, but will that continue throughout the year?
by
Brian Bailey
Balancing Training, Quantization, And Hardware Integration In NPUs
Evolving challenges and strategies in AI/ML model deployment and hardware optimization have a big impact on NPU architectures.
by
Ann Mutschler
Noise: A Chip Killer
Concern is growing in complex designs where there are few dedicated tools to help find and deal with it.
by
Brian Bailey
Power Integrity And Voltage Issues Get Harder To Detect And Solve
Inconsistent demand from multiple features can greatly increase the number of corner cases.
by
Ann Mutschler
Chiplets And 3D-ICs Add New Electrical And Mechanical Challenges
Reliability is now a system-level concern that includes everything from materials and packaging to testing with backside power.
by
Ann Mutschler
Sponsors
Advertise with us
Advertise with us
Advertise with us
Newsletter Signup
Popular Tags
2.5D
5G
advanced packaging
AI
AMD
ANSYS
Apple
Applied Materials
ARM
Arteris
automotive
business
Cadence
chiplets
EDA
eSilicon
EUV
GlobalFoundries
Google
IBM
imec
Infineon
Intel
IoT
IP
Keysight
Lam Research
machine learning
memory
Mentor
Mentor Graphics
MIT
Nvidia
NXP
Qualcomm
Rambus
Samsung
security
SEMI
Siemens
Siemens EDA
Synopsys
test
TSMC
verification
Recent Comments
Freelancer
on
Chip Industry Talent Shortage Drives Academic Partnerships
Chris Riches
on
Backside Power Delivery Creates Fab Tool, Thermal Dissipation Barriers
Jon
on
Robust Dynamic Voltage Droop Mitigation And Power Management
Ashfaq
on
Minimum Energy Per Query
Robert Boissy
on
Can A Computer Science Student Be Taught To Design Hardware?
Hank Walker
on
Can A Computer Science Student Be Taught To Design Hardware?
fieke khan
on
Bump Co-Planarity And Inconsistencies Cause Yield, Reliability Issues
Rajiv
on
Chip Industry Week in Review
Guy van der Walt - Thermco
on
Chiplets And 3D-ICs Add New Electrical And Mechanical Challenges
Stephen W
on
Chiplet Fundamentals For Engineers: eBook
ShrdMem256
on
The Verification Conundrum
Brendan McGuire
on
Wafer Probe Struggles To Adapt To Multi-Die Assemblies
NobodyTestedThis
on
The Verification Conundrum
Fiber Techs San Francisco
on
Agentic AI In Chip Manufacturing
SF Fiber Techs
on
Oxides Bring Low Leakage Transistors To Leading-Edge Memories
humic
on
Addressing Critical Tradeoffs In NPU Design
Dr. Dev Gupta
on
Liquid Cooling Gains Traction In Data Centers
Mikko Utriainen, Chipmetrics
on
Metrology Digs Deep To Produce Next-Generation 3D NAND
Raymond Doerr
on
Wafer Bonding Mechanisms Using SiCN Films For Hybrid Bonding Applications In 3D Integration
Hoyong Lee
on
Chiplets Vs. Soft IP: Different In Almost Every Way
Nano Banana AI
on
Blog Review: Dec. 17
JS Paek
on
Thermal Management In 3D-IC: Modeling Hotspots, Materials, & Cooling Strategies
Larry K
on
Chiplets Vs. Soft IP: Different In Almost Every Way
Seceon.Inc
on
Resilient And Optimized GenAI Systems
Linda Christensen
on
AI With Open And Scaled Data Sharing in IC Manufacturing (NIST)
komputer
on
AI With Open And Scaled Data Sharing in IC Manufacturing (NIST)
Sree
on
The Thermal Trap: How Dielectrics Limit Device Performance
David Muncier
on
China GenAI: Who Will Fill The Vacuum?
acp
on
Is There Still a Future for Hard Disk Drives?
Carlos Borer
on
Legacy Process Nodes Going Strong
Raj Sodhi
on
AI Meets Device Modeling: Transforming Compact Modeling With Machine Learning
Jaynarayan Tudu
on
Semiconductor Test Faces Technology Shifts In The AI Era
Mihai Buta
on
Why In-Memory Computation Is So Important For Edge AI
Silver Luis
on
The Competitive Advantage Of SRAM PUF Technology
Gretchen Patti
on
Advanced Packaging: A Key Technology For The Next Generation Of Electronics
Ev roach
on
AI Bubble Or Boom?
Kathleen Murphy-Weber
on
Chip Industry Week in Review
Raz
on
Multi-Die Verification
Paul C
on
Scaling Memory With Molybdenum
JWS
on
Scaling Memory With Molybdenum
Klein miller
on
Electrifying Everything: Power Moves Toward ICs
Team at Rise Design Automation
on
What Does Semiconductor Disruption Look Like?
masa mizuno
on
Physics Limits Interposer Line Lengths
Lou Covey
on
What Does Semiconductor Disruption Look Like?
Ricardo Shiroma
on
Complex Mix Of Processors At The Edge
Cor
on
Glass Substrates Gain Momentum
Daya Young
on
New Antennas And Advanced ICs Needed For 6G
Subramanian Srikanteswara Iyer
on
Manufacturing At The Limits
Doug La Tulipe
on
Coloring Optical Signals For More Bandwidth In Data Centers
WH
on
The Hidden Cost Of Contact Resistance
Raymond Doerr
on
Metrology Under Pressure: Detecting Defects in Fine-Pitch Hybrid Bonding
Raymond Doerr
on
Manufacturing At The Limits
Mallikarjun
on
The Evolution of DRAM
Klein Miller
on
Democratizing Design: How The CHIPS Act Is Reshaping EDA And Semiconductor Innovation
Klein Miller
on
Lessons From 30 Years In The Trenches On The Future Of Semiconductor Manufacturing
Jonathan Kolber
on
Preparing For The Quantum Computing Age
Pramod Gupta
on
Challenges In Stacking HBM
Madeline Lueilwitz
on
Reconfigurable Single-Walled CNT FeFET (Univ. of Pennsylvania, Yonsei et al.)
Anne Meixner
on
Need For KGD Drives Singulated Die Screening
Capt kirk
on
Designing A Better Clock Network
Alex Martin
on
AI Effort And Money Misplaced
Hamilton Carter
on
AI Effort And Money Misplaced
Ilmu Komunikasi
on
Reconfigurable Single-Walled CNT FeFET (Univ. of Pennsylvania, Yonsei et al.)
Giovanni Lostumbo
on
Will New Processor Architectures Raise Energy Efficiency?
Brendon Berg
on
ESD Guns, Transients And Testing…Oh My!
GD
on
All About Interconnects
Raimo
on
Crisis Ahead: Power Consumption In AI Data Centers
Fred Chen
on
Laser-Focused Results: Improving EUV Line Edge Roughness With Ion Beam Etching
Fred Chen
on
Many Options For EUV Photoresists, No Clear Winner
Amba Prasad
on
Advanced Packaging Fundamentals for Semiconductor Engineers: eBook
Shakir Ullah
on
The Race To Replace Silicon
Hwaiyu Geng, P.E.
on
Accelerating Semiconductor Process Development Using Virtual Design Of Experiments
Larry Gus Christiansen
on
Reducing Risk In The Semiconductor Supply Chain
Vikas Sharma
on
RTL Signoff vs. Functional Signoff: What’s The Difference?
Simone
on
Crisis Ahead: Power Consumption In AI Data Centers
Ron Lavallee
on
Can Today’s Processor Architectures Be More Efficient?
Rashid
on
Can Today’s Processor Architectures Be More Efficient?
Joseph Fjelstad
on
When Can I Buy A Chiplet?
Craig Lytle
on
Can Today’s Processor Architectures Be More Efficient?
Partha Thirumalai
on
Cognichip: Using AI To Speed Complex Chip Design
Gopal raju
on
Advanced Packaging Fundamentals for Semiconductor Engineers: eBook
Lawrence Kushner
on
Democratizing Design: How The CHIPS Act Is Reshaping EDA And Semiconductor Innovation
Ken Rygler
on
Disruptive Changes Ahead For Photomasks?
Jan Hoppe
on
Need For KGD Drives Singulated Die Screening
B.S. DeepakSubramanyan
on
HBM Roadmap: Next-Gen High-Bandwidth Memory Architectures (KAIST’s TERALAB)
Dr. Subhash L. Shinde , Booz Allen, Ex. Univ. of Notre Dame, Ex. Sandia National Labs., Ex. IBM.
on
The Race To Glass Substrates
Traian MUNTEAN (Honorary Professor)
on
A Balanced Approach To Verification
Amba Prasad
on
HBM Roadmap: Next-Gen High-Bandwidth Memory Architectures (KAIST’s TERALAB)
sam
on
HBM Roadmap: Next-Gen High-Bandwidth Memory Architectures (KAIST’s TERALAB)
Lentz
on
Agentic AI In Chip Design
adam
on
RISC-V’s Increasing Influence
Jon Taylor
on
RISC-V’s Increasing Influence
Roi Mit
on
The DAC Valuation
Janis Robin Schamberger
on
Chip Industry Week in Review
Rashid Kukkady
on
New Data Center Protocols Tackle AI
Peter Bennet
on
The DAC Valuation
Dan Ganousis
on
Optimizing Data Movement
DFTguy
on
Revolutionizing Semiconductor Development With GPU-Enhanced Atomistic Modeling
1945x
on
Laser-Focused Results: Improving EUV Line Edge Roughness With Ion Beam Etching
Jason Kennerly
on
Many Options For EUV Photoresists, No Clear Winner
Marc Swinnen
on
Development Flows For Chiplets
Warren Savage
on
Development Flows For Chiplets
N. L. Kamaruzzaman
on
Security Risks Mount For Aerospace, Defense Applications
IT
on
Three-Way Race To 3D-ICs
Marzieh SalarRahimi
on
Advanced Packaging Fundamentals for Semiconductor Engineers: eBook
Harry Foster
on
Tape-Out Failures Are The Tip Of The Iceberg
Brian Bailey
on
Tape-Out Failures Are The Tip Of The Iceberg
Purple music
on
Tape-Out Failures Are The Tip Of The Iceberg
Messika
on
Tape-Out Failures Are The Tip Of The Iceberg
Al
on
Tape-Out Failures Are The Tip Of The Iceberg
Svetlana Morozova
on
GPU Analysis Identifying Performance Bottlenecks That Cause Throughput Plateaus In Large-Batch Inference
universitywafer
on
Advancements In Silicon Device Technology And Design Driving New SLM Monitor Categories
Dr. Dev Gupta
on
Packaging With Fewer People And Better Results
Michael Current
on
Advanced Packaging Fundamentals for Semiconductor Engineers: eBook
Jack G
on
3D-IC For The Masses
Marc Greenberg
on
Implementing AI Activation Functions
Dr. D.
on
Big Changes Ahead For Interposers And Substrates
Dante
on
GPU Or ASIC For LLM Scale-Up?
Gretchen Patti
on
What Exactly Are Chiplets And Heterogeneous Integration?
Rob McCance
on
The Seven Pillars Of IC Package Physical Design
Marketplace T
FeFETs With Laminated Gate Stack...
Technical Paper Link
The Specialty Device Surge, Part...
Christopher Haire
About
About us
Contact us
Advertising on SemiEng
Newsletter SignUp
Navigation
Homepage
Special Reports
Systems & Design
Low Power-High Perf
Manufacturing, Packaging & Materials
Test, Measurement & Analytics
Auto, Security & Enabling Technologies
Videos
Jobs
Technical Papers
Events
Webinars
Knowledge Centers
Industry Research
Business & Startups
Newsletters
Store
Connect With Us
Facebook
Twitter
@semiEngineering
LinkedIn
YouTube
Copyright ©2013-2026 SMG   |
Terms of Service
|
Privacy Policy
This site uses cookies. By continuing to use our website, you consent to our
Cookies Policy
ACCEPT
Manage consent
Close
Privacy Overview
This website uses cookies to improve your experience while you navigate through the website. The cookies that are categorized as necessary are stored on your browser as they are essential for the working of basic functionalities of the website. We also use third-party cookies that help us analyze and understand how you use this website. We do not sell any personal information.
By continuing to use our website, you consent to our Privacy Policy. If you access other websites using the links provided, please be aware they may have their own privacy policies, and we do not accept any responsibility or liability for these policies or for any personal data which may be collected through these sites. Please check these policies before you submit any personal information to these sites.
Necessary
Necessary
Always Enabled
Necessary cookies are absolutely essential for the website to function properly. This category only includes cookies that ensures basic functionalities and security features of the website. These cookies do not store any personal information.
Non-necessary
Non-necessary
Any cookies that may not be particularly necessary for the website to function and is used specifically to collect user personal data via analytics, ads, other embedded contents are termed as non-necessary cookies. It is mandatory to procure user consent prior to running these cookies on your website.
SAVE & ACCEPT