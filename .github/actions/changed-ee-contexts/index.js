const core = require('@actions/core');

try {
  const changed_files = core.getInput('changed-files');

  console.log(changed_files);
  if (changed_files === undefined || changed_files === '') {
    core.setOutput("changed-ees", []);
    return;
  } 

  const changed_ees = changed_files
    .split(" ")
    .map(f => f.split("/")[1]);
    
  const deduped_ees = [...new Set(changed_ees)];
  console.log(deduped_ees);
  core.setOutput("changed-ees", deduped_ees);

} catch (error) {
  core.setFailed(error.message);
}