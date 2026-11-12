import { AxiosRequestConfig } from 'axios';
import {
  KnowledgeDocument,
  UploadDocumentParams,
  CreateKnowledgeParams,
  AddKnowledgeUrlParams,
  UploadKnowledgeFileParams,
} from '../types';

export class Knowledge {
  constructor(private request: <T = any>(config: AxiosRequestConfig) => Promise<T>) {}

  /**
   * Create a knowledge document from plain text (JSON body).
   * Prefer this for guided Q&A so `retrieve` returns readable `content`.
   *
   * @example
   * const doc = await pollax.knowledge.create({
   *   name: 'Fees FAQ',
   *   content: 'Annual tuition is ₹45,000.',
   *   type: 'txt',
   * });
   */
  async create(params: CreateKnowledgeParams): Promise<KnowledgeDocument> {
    return this.request<KnowledgeDocument>({
      method: 'POST',
      url: '/api/v1/knowledge',
      data: {
        name: params.name,
        content: params.content,
        type: params.type || 'txt',
        ...(params.agent_id ? { agent_id: params.agent_id } : {}),
      },
    });
  }

  /**
   * Upload a document to the knowledge base (multipart POST /knowledge).
   *
   * @example
   * const doc = await pollax.knowledge.upload({
   *   name: 'Product Manual',
   *   file: pdfFile,
   *   type: 'pdf',
   * });
   */
  async upload(params: UploadDocumentParams): Promise<KnowledgeDocument> {
    const formData = new FormData();
    formData.append('name', params.name);

    if (params.file) {
      formData.append('file', params.file as any);
    }
    if (params.content) {
      formData.append('content', params.content);
    }
    if (params.url) {
      formData.append('url', params.url);
    }
    if (params.type) {
      formData.append('type', params.type);
    }
    if (params.agent_id) {
      formData.append('agent_id', params.agent_id);
    }

    return this.request<KnowledgeDocument>({
      method: 'POST',
      url: '/api/v1/knowledge',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  /**
   * Upload a file via POST /knowledge/upload (binary ingest path).
   *
   * @example
   * const doc = await pollax.knowledge.uploadFile(buffer, {
   *   filename: 'handbook.pdf',
   *   agent_id: 'agent_123',
   * });
   */
  async uploadFile(
    file: File | Buffer | Blob,
    params: UploadKnowledgeFileParams = {},
  ): Promise<KnowledgeDocument> {
    const formData = new FormData();
    const filename = params.filename || 'document.bin';
    // Node FormData / undici accept (blob, filename); browsers take File directly.
    if (typeof Blob !== 'undefined' && file instanceof Blob && !(file instanceof File)) {
      formData.append('file', file, filename);
    } else if (typeof Buffer !== 'undefined' && Buffer.isBuffer(file)) {
      formData.append('file', new Blob([file]), filename);
    } else {
      formData.append('file', file as any, filename);
    }
    if (params.name) formData.append('name', params.name);
    if (params.agent_id) formData.append('agent_id', params.agent_id);

    return this.request<KnowledgeDocument>({
      method: 'POST',
      url: '/api/v1/knowledge/upload',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      maxBodyLength: Infinity,
      maxContentLength: Infinity,
    } as AxiosRequestConfig);
  }

  /**
   * Ingest knowledge from a public URL.
   *
   * @example
   * await pollax.knowledge.addUrl({ url: 'https://school.edu/fees', name: 'Fees' });
   */
  async addUrl(params: AddKnowledgeUrlParams): Promise<KnowledgeDocument> {
    return this.request<KnowledgeDocument>({
      method: 'POST',
      url: '/api/v1/knowledge/url',
      data: params,
    });
  }

  /**
   * Knowledge base aggregate stats for the account.
   */
  async stats(): Promise<Record<string, any>> {
    return this.request({
      method: 'GET',
      url: '/api/v1/knowledge/stats',
    });
  }

  /**
   * List all knowledge documents
   *
   * @example
   * const documents = await pollax.knowledge.list();
   */
  async list(): Promise<KnowledgeDocument[]> {
    const res = await this.request<KnowledgeDocument[] | { data?: KnowledgeDocument[] }>({
      method: 'GET',
      url: '/api/v1/knowledge',
    });
    return Array.isArray(res) ? res : (res?.data ?? []);
  }

  /**
   * Get a single document by ID (includes readable `content` when available).
   *
   * @example
   * const doc = await pollax.knowledge.retrieve('doc_123');
   */
  async retrieve(documentId: string): Promise<KnowledgeDocument> {
    return this.request<KnowledgeDocument>({
      method: 'GET',
      url: `/api/v1/knowledge/${documentId}`,
    });
  }

  /**
   * Delete a document
   *
   * @example
   * await pollax.knowledge.delete('doc_123');
   */
  async delete(documentId: string): Promise<{ success: boolean }> {
    return this.request({
      method: 'DELETE',
      url: `/api/v1/knowledge/${documentId}`,
    });
  }

  /**
   * Search the knowledge base
   *
   * @example
   * const results = await pollax.knowledge.search({
   *   query: 'How do I reset my password?',
   *   limit: 5,
   * });
   */
  async search(params: { query: string; limit?: number }): Promise<{
    results: Array<{
      document_id: string;
      content: string;
      score: number;
    }>;
  }> {
    return this.request({
      method: 'POST',
      url: '/api/v1/knowledge/search',
      data: params,
    });
  }
}
