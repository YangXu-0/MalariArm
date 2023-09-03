# MalariArm
Contains some of the artifacts and files from my Praxis III design Project. <br />
In Praxis III, I worked with a team of other Engineering Science students to create a something to help combat the malaria problem in Nigeria. 

### The Problem <br />
After a lot of research and talking with stakeholders, we realized that there were several problems healthcare officials faced when treating malaria. Problems included:
1. Lack of access to accurate testing methods due to price constraints.
2. Reaching citizens in rural locations.
3. Wide-spread administration of malaria treatment without proper diagnosis due to the rapid nature of malaria and slow testing processes. 

Looking at these problems, there is clearly an issue with malaria testing, so that's what we decided to work on. Currently, the most accurate way of testing for malaria is to look for parasites in blood samples. This is a long and expensive process because a blood sample from a patient needs to be manually put through a long chemical staining process before it can be examined for malaria. We wanted to automate the repetitive chemical staining process so that technicians can focus on the skilled aspect of identifying malaria parasites rather than waste time and money on a trivial task. With reduced costs, more patients can be tested accurately and recieve correct treatment. 

### Our Approach <br />
Our approach to this problem of inefficiency was to design a robotic arm. The idea is that using some microcontrollers, 3D printing, and some motors, we can build an affordable robotic arm to automatically prepare blood samples for inspection. The technicians will leave raw blood samples in containers, which the robotic arm will pickup and drop into containers of chemicals to stain them before picking them out and leaving them to dry for the technicians. Samples need to be left in chemicals for specified periods of time (ex. 5 minutes). Normally, this limits technicians to preparing just 1-2 samples at once, but with some basic software, the robotic arm can track and prepare several samples at the same time.

### Our Design <br />
The general design of the robotic arm is simple. We have a microcontroller that runs through some logic and sends instructions to 2 motors to control the arm. One motor turns a series of gears to rotate the central cylinder of the arm (Rotational Translation System). The other motor turns a spool of string to move a small arm up and down to reach the containers (Vertical Translation System). To pickup the containers, we attached a magnet in both the arm and the lid of each container so that the arm will just stick to the containers when close enough. Once the container is the in the right spot, the magnet can be easily disengaged by rotating the arm before moving it upwards to slide the magnet off the lid. This is far more simple, and thus accessible, attachment system than a robotic pincher.

In the end, we were able to build a simple working prototype of our idea. Since we only used cheap materials (PLA for gears and such, some cheap wood, and some string), 2 motors, and a microcontroller, it only cost us about $67 or ₦22797 to build, which is very affordable based on our research. 

Credit to my teammates: Gerry Zhu, Eugene Lee, Joaquin Arcilla, and Liam Ernst-Selway

Here is a quick demo of our prototype system.

https://github.com/YangXu-0/MalariArm/assets/82414709/51cae7a8-68f9-47df-8178-39f1a8b26d3f

