# Summarizing pdf documents
*This is still under development, so please excuse the shoddiness*  
## Aim
To summarize a pdf document (input used here is an ESG report). ESG reports are full of lot of jargon and look chirpy and quite the same, but underneath they hide quite a lot of info. So rather than have an analyst read pages of this report, how about creating a summary per page
## Files
**Ignore**  
- txt files are sandboxes (ignore)
- summarize_old.py (ignore, 1st version)
- summarize_try.py (ignore, 1st version)
- refCode.py (ignore, example code)

- summarize_cosine.py (summarizes by the cosine similarity method)
- summarize_weighted.py (summarizes by the word weights)
- pdfs are inputs 
## Code
The code uses ESG documents of JP Morgan (jpm.pdf) and Goldman Sachs (gs.pdf) as input. 

## TODO:
- Write a better Readme :P
- The Alibaba document has an interesting format and I must think of a smart way to get relevant text out 
- Need to make the code clean and usable
- Understand the technique (cosine) better, this is still an implementation
- Make summary of the entire pdf (executive summary)
- Make summary per page and stitch them together (extended summary per page)
- Get sentiment (overall/per page??)
- Test with an audience
