/**
 * Simple YAML parser for infrastructure configuration.
 */

const fs = require('fs');
const path = require('path');
const yaml = require('yaml');
const core = require('@actions/core');
const {
  context
} = require('@actions/github');
const config = require('./pipe_config.json')

const ENVIRONMENTS = ["dev", "prod"]

/**
 * Main function for GitHub Action
 */
async function run() {
    // Get inputs from the action
    let pipeConfig = Object.assign({}, config.global);
    pipeConfig.app_name = core.getInput('app_name');
    pipeConfig.current_env = core.getInput('current_env') || 'dev';
    pipeConfig.is_promote = core.getBooleanInput('is_promote');
    pipeConfig.app_version = core.getInput('app_version');

    validate(pipeConfig);
    setGlobalValues(pipeConfig);
    const infraFileValue = getChartFileValue(`./infra/${pipeConfig.current_env}.yaml`);
    setSteps(pipeConfig, context.eventName);
    setEnvironmentDetails(pipeConfig);

  if (infraFileValue) {
    setResourceConfig(pipeConfig, infraFileValue);
  }
  console.log(JSON.stringify(pipeConfig, null, 2));
  core.setOutput("pipe_config", pipeConfig);
}

/**
 * Validate pipeline inputs and throw error if values are missing
 * @param {*} pipeConfig 
 */
function validate(pipeConfig) {
  if (!ENVIRONMENTS.includes(pipeConfig.current_env)) {
    throw new Error(`Invalid environment ${pipeConfig.current_env}, valid environments are ${ENVIRONMENTS}`);
  }
}

/**
 * Set pipeline global values
 * 
 * @param {*} pipeConfig 
 */
function setGlobalValues(pipeConfig) {
  if (pipeConfig.is_promote) {
    //If it is promote default branch to main and image registry to release channel
    pipeConfig.branch = 'main';
    pipeConfig.image_registry = `${pipeConfig.image_registry}/release/${pipeConfig.repo}`;
  } else {
    pipeConfig.repo = process.env["GITHUB_REPOSITORY"].split('/').pop().trim();

    pipeConfig.branch = process.env["GITHUB_REF_NAME"].trim();
    
    let channel = pipeConfig.branch == 'main' ? "release" : "snapshot";

    pipeConfig.image_registry = `${pipeConfig.image_registry}/${channel}/${pipeConfig.repo}`;
    pipeConfig.version = process.env["GITHUB_SHA"].substring(0, 6);
  }
}

/**
 * Compute pipeline steps to be executed and set to pipeConfig
 */
function setSteps(pipeConfig, eventName) {
  var steps = config.steps;
  if(pipeConfig.is_promote){
    console.log("Setting steps in isPromote ")
    Object.keys(steps).forEach(key => {
      steps[key] = false;
    });    
    steps.deploy = true;
  } else {
    steps.test = true;
    steps.build = true;
    steps.deploy = true;
    if (pipeConfig.branch == 'main') {
      steps.tag = true;
      steps.publish = true;
    } else {
      steps.tag = false;
      steps.publish = false;
    }
  }
  pipeConfig.steps = steps;
}

/**
 * Read base-values.yaml file and return the values of infra-config
 * @returns values of infra-config otherwise null
 */
function getChartFileValue(baseFileLocation) {
  if (fs.existsSync(baseFileLocation)) {
    var baseFile = yaml.load(fs.readFileSync(baseFileLocation, 'utf8'));
    if (baseFile && baseFile["infra-config"]) {
      return baseFile["infra-config"];
    }
  }
  return null;
}


/**
 * Set environment details based on selected environment
 * @param {*} pipeConfig 
 */
function setEnvironmentDetails(pipeConfig) {
  pipeConfig = Object.assign(pipeConfig, config[pipeConfig.current_env]);
}


/**
 * Set computed resource value from base-values.yaml
 * 
 * @param {*} pipeConfig 
 * @param {*} infraFileValue 
 */
function setResourceConfig(pipeConfig, infraFileValue) {
  pipeConfig.db_migration = getDBMigration(pipeConfig.branch, infraFileValue);
  pipeConfig.deploymentDetail = getDeploymentDetail(pipeConfig, infraFileValue);
}


/**
 * Get postgres computed values from infra/env.yaml
 * @param {*} branch 
 * @param {*} infraFileValue 
 * @returns 
 */
function getDBMigration(branch, infraFileValue) {

  let db_migration = config.db_migration;

  postgres(infraFileValue, db_migration, branch);

  return db_migration;
}


function postgres(infraFileValue, db_migration, branch) {
  if (infraFileValue?.postgres?.enabled) {
    db_migration.postgres.enabled = true;
    if (infraFileValue.postgres?.flywayDbMigrationPath) {
      db_migration.postgres.sqlPath = infraFileValue.postgres.flywayDbMigrationPath;
      console.log("Is sql path found ", fs.existsSync(db_migration.postgres.sqlPath));
    }
    if (infraFileValue.postgres?.username) {
      db_migration.postgres.username = infraFileValue.postgres.username;
    } else {
      throw new Error("postgres is enabled but database username is not provided");
    }
    if (infraFileValue.postgres?.instanceName) {
      db_migration.postgres.instanceName = infraFileValue.postgres.instanceName;
    } else {
      throw new Error("postgres is enabled but instanceName is not provided");
    }
    if (infraFileValue.postgres?.database) {
      if (["main"].includes(branch) || !db_migration.postgres.sqlPath) {
        db_migration.postgres.database = infraFileValue.postgres.database;
      }
    } else {
      throw new Error("postgres is enabled but database name is not provided");
    }
  }
}

/**
 * Get deployment config
 * @param {*} pipeConfig 
 * @param {*} infraFileValue 
 * @returns 
 */
function getDeploymentDetail(pipeConfig, infraFileValue) {
  var deploymentDetail = Object.assign({}, config.deploymentDetail);
  deploymentDetail.details = [];
    deploymentDetail.isMultiDeploy = false;
    const overrideVal = getChartFileValue(`./infra/${pipeConfig.current_env}.yaml`);

    deploymentDetail.details.push({
      "appName": pipeConfig.repo,
      "postfix": null,
      "isInfraDeploy": infraFileValue?.infraResources ? true : overrideVal?.infraResources ? true : false,
    });
  return deploymentDetail;
}



// Run the action if this is the main module
run().catch(error => {
  core.setFailed(error);
  console.error(error);
})