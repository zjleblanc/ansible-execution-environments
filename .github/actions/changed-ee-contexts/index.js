const core = require('@actions/core');

try {
  const changed_files = core.getInput('changed-files');

  console.log(changed_files);
  if (changed_files === undefined || changed_files === '') {
    core.setOutput("changed-ees", ['no-op']);
    core.setOutput("changed-ees-count", 0);
    return;
  } 

  const changed_ees = changed_files
    .split(" ")
    .map(f => f.split("/")[0]);

  const deduped_ees = [...new Set(changed_ees)];
  console.log(deduped_ees);
  core.setOutput("changed-ees", deduped_ees);
  core.setOutput("changed-ees-count", deduped_ees.length);

} catch (error) {
  core.setFailed(error.message);
}