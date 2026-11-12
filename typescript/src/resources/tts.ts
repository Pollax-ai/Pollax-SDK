import { AxiosRequestConfig } from 'axios';
import { BroadcastPreviewParams, BroadcastPreviewResult } from '../types';

export class Tts {
  constructor(private request: <T = any>(config: AxiosRequestConfig) => Promise<T>) {}

  /**
   * Preview one-way broadcast TTS audio (language + speed).
   *
   * @example
   * const preview = await pollax.tts.broadcastPreview({
   *   text: 'School will be closed tomorrow.',
   *   language: 'hi',
   *   speed: 1,
   * });
   */
  async broadcastPreview(params: BroadcastPreviewParams): Promise<BroadcastPreviewResult> {
    return this.request<BroadcastPreviewResult>({
      method: 'POST',
      url: '/api/v1/tts/broadcast-preview',
      data: params,
    });
  }
}
