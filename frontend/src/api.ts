export interface Meta {
  title: string;
  when: string;
  where: string;
  note: string;
}

export interface OverviewStats {
  participant_count: number;
  coming_headcount: number;
  dish_count: number;
  open_dish_count: number;
  claimed_dish_count: number;
}

export interface Overview {
  meta: Meta;
  stats: OverviewStats;
}

export interface Participant {
  id: string;
  name: string;
  headcount: number;
  status: string;
  note: string;
}

export interface SignupTask {
  id: string;
  name: string;
}

export interface Signup {
  participant: Participant;
  task: SignupTask | null;
}

export interface SignupCreate {
  name: string;
  task: string;
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
  listSignups: () => request<Signup[]>("/api/signups"),
  createSignup: (body: SignupCreate) =>
    request<Signup>("/api/signups", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  deleteSignup: (participantId: string) =>
    request<void>(`/api/signups/${participantId}`, { method: "DELETE" }),
};
