import { AxiosRequestConfig } from 'axios';
import { WalletBalance, WalletLedgerParams, WalletLedgerPage } from '../types';

export class Wallet {
  constructor(private request: <T = any>(config: AxiosRequestConfig) => Promise<T>) {}

  /**
   * Get current wallet balance (INR / paise).
   *
   * @example
   * const wallet = await pollax.wallet.get();
   * console.log(wallet.balance_inr);
   */
  async get(): Promise<WalletBalance> {
    return this.request<WalletBalance>({
      method: 'GET',
      url: '/api/v1/wallet',
    });
  }

  /** Alias for {@link Wallet.get}. */
  async retrieve(): Promise<WalletBalance> {
    return this.get();
  }

  /**
   * List wallet ledger entries (charges, top-ups).
   *
   * @example
   * const page = await pollax.wallet.ledger({ limit: 50 });
   */
  async ledger(params?: WalletLedgerParams): Promise<WalletLedgerPage> {
    return this.request<WalletLedgerPage>({
      method: 'GET',
      url: '/api/v1/wallet/ledger',
      params,
    });
  }
}
