- Add support for better logging
- Add support for other source of data ingestion
- Add support for multiple file format
- Add support for cloud storage
- Finalize the config file structure

## Simple Flow (MVP)

- Load config and build context object
- Validate steps mentioned in the config can be processed or not.
- Build Pipeline
- Execute Pipeline
- Store information in mlflow artifacts

## After MVP tasks

- Rather than linear approach for pipeline execution try dag
- Add UI for config building (Session takes input from ui build config file in yaml.) Optional Store this in DB If needed.
-

## Need to implement or Improve

- improve: Each object is storing reference of Context (RunContext)

## Implement Proper error handling

- Define any error classes if needed.
- Handling of errors in preprocessing pipeline
- Fix Logging, better logging
- Add tracker for pipelines

- p0

## Future Enhancements

- Build for multiple models eg -> text input -> tf-idf -> classification