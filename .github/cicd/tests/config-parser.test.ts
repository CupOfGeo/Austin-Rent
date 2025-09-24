/**
 * Unit tests for config-parser module.
 */

import { parseConfig, InfraConfig, ParsedConfig } from '../config-parser';

describe('parseConfig', () => {
  describe('when parsing a complete configuration with all fields present', () => {
    it('should correctly parse all fields', () => {
      const inputConfig: InfraConfig = {
        appName: 'my-app',
        uses_db: true,
        secrets: { KEY1: 'encrypted_value1', KEY2: 'encrypted_value2' },
        env_vars: { ENVIRONMENT: 'prod', DEBUG: 'false' }
      };

      const result = parseConfig(inputConfig);

      const expected: ParsedConfig = {
        app_name: 'my-app',
        uses_db: true,
        secrets: { KEY1: 'encrypted_value1', KEY2: 'encrypted_value2' },
        env_vars: { ENVIRONMENT: 'prod', DEBUG: 'false' }
      };

      expect(result).toEqual(expected);
    });
  });

  describe('when parsing minimal config with defaults', () => {
    it('should apply proper defaults for missing fields', () => {
      const inputConfig: InfraConfig = {
        appName: 'minimal-app'
      };

      const result = parseConfig(inputConfig);

      const expected: ParsedConfig = {
        app_name: 'minimal-app',
        uses_db: false,  // Default should be false
        secrets: {},     // Default should be empty object
        env_vars: {}     // Default should be empty object
      };

      expect(result).toEqual(expected);
    });
  });

  describe('when parsing config with missing appName', () => {
    it('should use empty string as default', () => {
      const inputConfig: InfraConfig = {
        uses_db: true
      };

      const result = parseConfig(inputConfig);

      expect(result.app_name).toBe('');
      expect(result.uses_db).toBe(true);
    });
  });

  describe('when parsing config with partial fields', () => {
    it('should handle secrets without env_vars', () => {
      const inputConfig: InfraConfig = {
        appName: 'partial-app',
        secrets: { API_KEY: 'secret123' }
      };

      const result = parseConfig(inputConfig);

      expect(result.app_name).toBe('partial-app');
      expect(result.uses_db).toBe(false);
      expect(result.secrets).toEqual({ API_KEY: 'secret123' });
      expect(result.env_vars).toEqual({});
    });

    it('should handle env_vars without secrets', () => {
      const inputConfig: InfraConfig = {
        appName: 'env-app',
        env_vars: { NODE_ENV: 'production' }
      };

      const result = parseConfig(inputConfig);

      expect(result.app_name).toBe('env-app');
      expect(result.uses_db).toBe(false);
      expect(result.secrets).toEqual({});
      expect(result.env_vars).toEqual({ NODE_ENV: 'production' });
    });
  });
});