# Scope and Charter
## Identification

**Project Name:**

NRC Electron Microscope Tools

**Sponsor Details:**

```
Misa Hayashida
Research Officer
National Research Council at the University of Alberta
```

## Software Description
Three Python tools that are used with electron microscope labratory. The Alignment software will take electron microscope nanoparticle images and align and optimize them for tracking them around each image. The Nanomi Optics software will optimize electron microscope settings based on user input. The qEELS software takes a spectrogram image and outputs calibrated energy loss.

## Objectives
- Understand and document the legacy MATLAB implementations
- Translate MATLAB features to Python
- Maintain all functionality from the legacy project
- Use popular Python packages for GUI and scientific application
- Design of a familiar user interface to the legacy implementation
- Create a straightforward manual/documentation that is understandable for non-programmers
- Educating our client on software engineering practices

## Scope

**In scope**
- Creating the tools 
- Feeding input/data provided by the client into our tools

**Out of Scope**
- Using tools on actual electron microscopes

## Milestones
- Documenting and understanding the legacy code
- Minimum viable product for each of the scripts
- Get the product approved by the client to ensure quality
- Finalize documentation

## Major Deliverables
There are three MATLAB programs provided that need to be translated to Python.
1. Alignment Software
2. Nanomi optics
3. qEELS
## High Level Requirements

**Functional Requirements**

1. Alignment Software
   1. User loads images into software
   2. User indicates the location of particles in images
   3. Software produces aligned images by tracking particles between frames of rotation
2. Nanomi optics
   1. User inputs desired parameters for optics
   2. User requests optimized lense settings
   3. Software calculates and outputs optimized settings
3. qEELS
   1. User loads spectrogram image into software
   2. User indicates the loation of features on the spectrogram to the software
   3. User indicates that the software should detect fitted peaks of surface plasmon and bluk plasmon
   4. Outputs calibrated energy loss axis and transfer axis

**Non-Functional Requirements**

Performance
- Portable and ability to run on multiple operating systems

Development
- Delivered by early August
- Cannot used paid resources


## Technical Requirements
- Legacy project and new software have functionally equivalent outputs given the same input
- Use popular Python packages for GUI and scientific application
- Separate the GUI from backend

## User Requirements
- Ablity to run on the user computer/system
- Users can upload data to the system
- Users can use optimization tools

## Assumptions and Constraints
**Assumptions**
-  Supplied with the legacy scripts
-  Provided code works

**Constraints**
- Python is a requirement
- Time

## High-Level Risks
- Developers get sick/travel
- Client is unavailable
- Poor team synergy
- Bad estimation of task complexities
- Poor team/client communication
- Understanding MATLAB
- Not completing the project, leading to failure to create a product and failure of the course
- Time constraints

## Summary Schedule

Work Breakdown Structure

## Stakeholder List
- Misa Hayashida
- National Research Council
- University of Alberta
- University of British Columbia Okanagan
- Project Team
- Potential future users
  
## Approvals

Project Sponsor _______________________________________ 

Signature ________________________________ Date ________

<br>

Project Manager _______________________________________ 

Signature ________________________________ Date ________

