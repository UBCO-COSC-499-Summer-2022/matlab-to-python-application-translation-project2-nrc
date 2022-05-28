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
Three Python tools that are used with electron microscope labratory. The qEELS software takes a spectrogram image and outputs calibrated energy loss. The Nanomi Optics software will optimize electron microscope optics settings based on user provided parameters. The Alignment software will take electron microscope nanoparticle images and align and optimize them for tracking them around each image.

## Objectives
- Understand and document the legacy MATLAB implementations
- Translate MATLAB features to Python
- Maintain all functionality from the legacy project
- Design of a familiar user interface to the legacy implementation
- Create a straightforward manual/documentation that is understandable for non-programmers
- Exposing our client to formal software engineering practices

## Scope

**In scope**
- Creating the tools 
- Feeding input/data provided by the client into our tools

**Out of Scope**
- Using tools on actual electron microscopes

## Milestones

1. Port qEELS 
2. Port Nanomi optics
5. Port Alignment Software
6. Document usage of the softwares

## Functional Requirements

- Legacy project and new software have functionally equivalent outputs given the same input
- qEELS
   1. Software can accept spectrogram and feature locations
   2. Software can detect fitted peaks of surface and bulk plasmon
   3. Software can calculate calibrated energy loss axis and transfer axis
- Nanomi optics
   1. Software can accept desired paramters from user
   2. Software calculate optimized optics settings
- Alignment Software
   1. Software can accept many frames/images
   2. Software can automatically roughly the location of particles accross frames
   3. Software can accept manual adjustments to location of particles
   4. Software can calculate and aligned sequence of images

## Non-Functional Requirements

- Performance
  - Portable and ability to run on multiple operating systems
- Development
  - Delivered by early August
  - Cannot used paid resources
- Quality
  - Code must be linted and in a consistent format

## Technical Requirements
- Legacy software must be run, documented and analyzed
- MATLAB dependencies must be replaced
- New software must be written in python
- New software must use well-supported Python packages
- New software must be thoroughly tested
- The GUI will be seperated from backend

## User Requirements
- User can learn can learn how to use software quickly from documentation
- User who used the legacy software can pick up new software easily
- qEELS
   1. User can load spectrogram image into software
   2. User can indicate the location of features on the spectrogram to the software
   3. User can indicate that the software should detect fitted peaks of surface plasmon and bluk plasmon
   4. User can request calibrated energy loss axis and transfer axis from software
- Nanomi optics
   1. User inputs desired parameters for optics
   2. User can request optimized lense settings from software
- Alignment Software
   1. User can load images into software
   2. User can indicate the location of particles in images
   3. User can request aligned sequemce images from software

## Assumptions

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

