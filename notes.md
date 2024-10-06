- Create a organized section wise rules/instructions file.


Steps:
1. Retriever agent will write a sample report from the final deliverable.
2. Reviewer agent will review the report and provide feedback based on the rules provided.
3. Quality Control agent will listen to user feedback and either modify the current report, refetch documents or continue to next section.
4. Final Report agent will write the final report based on type of document.

TODO

- [x] Create a working graph with human in the loop
- [ ] Improve RAG ingestion
- [ ] Prompt Engineering

BUGS

1. Rewriting on feedback agent writes same content to file.