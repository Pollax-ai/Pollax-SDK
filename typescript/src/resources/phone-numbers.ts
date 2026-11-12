import { AxiosRequestConfig } from 'axios';
import {
  PhoneNumber,
  SearchPhoneNumbersParams,
  NumberRequest,
  NumberRequestParams,
  UpdatePhoneNumberParams,
  AssignPhoneNumberParams,
  ProvisionPhoneNumberParams,
} from '../types';

export class PhoneNumbers {
  constructor(private request: <T = any>(config: AxiosRequestConfig) => Promise<T>) {}

  /**
   * List all phone numbers
   *
   * @example
   * const numbers = await pollax.phoneNumbers.list();
   */
  async list(): Promise<PhoneNumber[]> {
    const res = await this.request<PhoneNumber[] | { data?: PhoneNumber[] }>({
      method: 'GET',
      url: '/api/v1/phone-numbers',
    });
    return Array.isArray(res) ? res : (res?.data ?? []);
  }

  /**
   * Search available phone numbers
   *
   * @example
   * const numbers = await pollax.phoneNumbers.search({
   *   country_code: 'US',
   *   area_code: '415',
   * });
   */
  async search(params: SearchPhoneNumbersParams): Promise<PhoneNumber[]> {
    const res = await this.request<PhoneNumber[] | { numbers?: PhoneNumber[]; data?: PhoneNumber[] }>({
      method: 'GET',
      url: '/api/v1/phone-numbers/search',
      params,
    });
    if (Array.isArray(res)) return res;
    return res?.numbers ?? res?.data ?? [];
  }

  /**
   * Purchase a phone number
   *
   * @example
   * const number = await pollax.phoneNumbers.purchase('+14155551234');
   */
  async purchase(phoneNumber: string): Promise<PhoneNumber> {
    return this.request<PhoneNumber>({
      method: 'POST',
      url: '/api/v1/phone-numbers',
      data: { phone_number: phoneNumber },
    });
  }

  /**
   * Update a owned phone number (e.g. auto-renew).
   *
   * @example
   * await pollax.phoneNumbers.update('num_123', { auto_renew: false });
   */
  async update(numberId: string, params: UpdatePhoneNumberParams): Promise<PhoneNumber> {
    return this.request<PhoneNumber>({
      method: 'PUT',
      url: `/api/v1/phone-numbers/${numberId}`,
      data: params,
    });
  }

  /**
   * Release a phone number
   *
   * @example
   * await pollax.phoneNumbers.release('num_123');
   */
  async release(numberId: string): Promise<{ success: boolean }> {
    return this.request({
      method: 'DELETE',
      url: `/api/v1/phone-numbers/${numberId}`,
    });
  }

  /**
   * Get the open "request my own number" ticket for this account, if any.
   */
  async getNumberRequest(): Promise<NumberRequest | null> {
    const res = await this.request<{ request?: NumberRequest | null }>({
      method: 'GET',
      url: '/api/v1/phone-numbers/number-request',
    });
    return res?.request ?? null;
  }

  /**
   * Ask Pollax support for a dedicated inbound number.
   *
   * @example
   * const { created, request } = await pollax.phoneNumbers.requestNumber({
   *   name: 'School Ops',
   *   email: 'ops@school.edu',
   * });
   */
  async requestNumber(
    params: NumberRequestParams = {},
  ): Promise<{ created: boolean; request: NumberRequest | null }> {
    const res = await this.request<{ created?: boolean; request?: NumberRequest | null }>({
      method: 'POST',
      url: '/api/v1/phone-numbers/number-request',
      data: params,
    });
    return {
      created: Boolean(res?.created),
      request: res?.request ?? null,
    };
  }

  /**
   * Assign a phone number to an agent (inbound routing).
   */
  async assign(numberId: string, params: AssignPhoneNumberParams): Promise<PhoneNumber> {
    return this.request<PhoneNumber>({
      method: 'POST',
      url: `/api/v1/phone-numbers/${numberId}/assign`,
      data: params,
    });
  }

  /**
   * Unassign a phone number from its agent.
   */
  async unassign(numberId: string): Promise<PhoneNumber> {
    return this.request<PhoneNumber>({
      method: 'POST',
      url: `/api/v1/phone-numbers/${numberId}/unassign`,
    });
  }

  /**
   * Provision inbound telephony for a number.
   */
  async provision(
    numberId: string,
    params?: ProvisionPhoneNumberParams,
  ): Promise<any> {
    return this.request({
      method: 'POST',
      url: `/api/v1/phone-numbers/${numberId}/provision`,
      data: params || {},
    });
  }

  /**
   * Deprovision inbound telephony for a number.
   */
  async deprovision(numberId: string): Promise<any> {
    return this.request({
      method: 'POST',
      url: `/api/v1/phone-numbers/${numberId}/deprovision`,
    });
  }
}
