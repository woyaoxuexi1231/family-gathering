export interface Meta {
  title: string;
  when: string;
  where: string;
  note: string;
}

export interface OverviewStats {
  entry_count: number;
  headcount_total: number;
}

export interface Entry {
  id: string;
  name: string;
  dish: string;
  headcount: number;
  note: string;
}

export interface Overview {
  meta: Meta;
  stats: OverviewStats;
  entries: Entry[];
}

export interface EntryCreate {
  name: string;
  dish: string;
  headcount: number;
  note: string;
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) detail = body.detail;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(detail, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  getOverview: () => request<Overview>("/api/overview"),
  listEntries: () => request<Entry[]>("/api/entries"),
  createEntry: (body: EntryCreate) =>
    request<Entry>("/api/entries", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  deleteEntry: (entryId: string) =>
    request<void>(`/api/entries/${entryId}`, { method: "DELETE" }),
};
