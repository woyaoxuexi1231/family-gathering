import { api, ApiError, type Entry, type Overview } from "./api";
import "./style.css";

type Flash = { kind: "ok" | "err"; text: string } | null;

interface AppState {
  overview: Overview | null;
  entries: Entry[];
  flash: Flash;
  loading: boolean;
}

const state: AppState = {
  overview: null,
  entries: [],
  flash: null,
  loading: true,
};

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("Missing #app root");

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderFlash(flash: Flash): string {
  if (!flash) return "";
  const cls = flash.kind === "ok" ? "flash flash--ok" : "flash flash--err";
  const role = flash.kind === "ok" ? "status" : "alert";
  return `<div class="${cls}" role="${role}">${escapeHtml(flash.text)}</div>`;
}

function renderEntryList(entries: Entry[]): string {
  if (entries.length === 0) {
    return `
      <div class="empty">
        <div class="empty__icon" aria-hidden="true">🍲</div>
        <p class="empty__title">还没有人报名</p>
        <p class="empty__hint">你是第一个的话，随便填一道拿手菜就行～</p>
      </div>
    `;
  }

  const items = entries
    .map((entry) => {
      const count =
        entry.headcount > 1
          ? `<span class="signup-card__count">${entry.headcount} 人</span>`
          : "";
      const note = entry.note
        ? `<p class="signup-card__note">${escapeHtml(entry.note)}</p>`
        : "";

      return `
        <li class="signup-card">
          <div class="signup-card__avatar" aria-hidden="true">${escapeHtml(entry.name[0] ?? "?")}</div>
          <div class="signup-card__body">
            <div class="signup-card__top">
              <strong class="signup-card__name">${escapeHtml(entry.name)}</strong>
              ${count}
            </div>
            <p class="signup-card__task">${escapeHtml(entry.dish)}</p>
            ${note}
          </div>
          <button type="button" class="btn btn--ghost btn--sm" data-delete="${escapeHtml(entry.id)}" data-name="${escapeHtml(entry.name)}">取消</button>
        </li>
      `;
    })
    .join("");

  return `<ul class="signup-list">${items}</ul>`;
}

function render(): void {
  const meta = state.overview?.meta;
  const stats = state.overview?.stats;

  app!.innerHTML = `
    <div class="page">
      <header class="hero">
        <div class="wrap hero__inner">
          <p class="hero__eyebrow">Family Gathering</p>
          <h1>${meta ? escapeHtml(meta.title) : "加载中…"}</h1>
          ${
            meta
              ? `
            <div class="hero__meta">
              <span class="hero__chip">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                ${escapeHtml(meta.when)}
              </span>
              <span class="hero__chip">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 21s7-4.5 7-11a7 7 0 1 0-14 0c0 6.5 7 11 7 11Z" stroke="currentColor" stroke-width="1.5"/>
                  <circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                ${escapeHtml(meta.where)}
              </span>
            </div>
            ${meta.note ? `<p class="hero__note">${escapeHtml(meta.note)}</p>` : ""}
          `
              : ""
          }
        </div>
      </header>

      <main class="wrap main">
        ${renderFlash(state.flash)}

        ${
          stats
            ? `
          <section class="stats" aria-label="聚餐概况">
            <div class="stat">
              <span class="stat__n">${stats.entry_count}</span>
              <span class="stat__l">已报名</span>
            </div>
            <div class="stat">
              <span class="stat__n">${stats.headcount_total}</span>
              <span class="stat__l">预计到场</span>
            </div>
          </section>
        `
            : ""
        }

        <section class="panel panel--form">
          <div class="panel__head">
            <h2>我要参加</h2>
            <p class="panel__desc">填上你是谁、自己做什么菜，就这一条信息。</p>
          </div>

          <form id="entry-form" class="signup-form">
            <div class="signup-form__row">
              <label class="field">
                <span class="field__label">你是谁</span>
                <input name="name" required maxlength="50" placeholder="小明" autocomplete="name">
              </label>
              <label class="field">
                <span class="field__label">你做什么菜</span>
                <input name="dish" required maxlength="80" placeholder="红烧肉">
              </label>
            </div>
            <div class="signup-form__row signup-form__row--compact">
              <label class="field field--narrow">
                <span class="field__label">几个人来</span>
                <input name="headcount" type="number" min="1" max="20" value="1">
              </label>
              <label class="field field--grow">
                <span class="field__label">备注（可选）</span>
                <input name="note" maxlength="200" placeholder="忌口、到达时间等">
              </label>
              <div class="field field--action">
                <span class="field__label field__label--hidden">提交</span>
                <button type="submit" class="btn btn--primary" ${state.loading ? "disabled" : ""}>报名参加</button>
              </div>
            </div>
          </form>
        </section>

        <section class="panel">
          <div class="panel__head panel__head--row">
            <div>
              <h2>报名列表</h2>
              <p class="panel__desc">谁来了、各自做什么菜。</p>
            </div>
            <span class="badge">${state.entries.length} 人</span>
          </div>
          ${state.loading ? `<p class="muted">加载中…</p>` : renderEntryList(state.entries)}
        </section>
      </main>

      <footer class="footer wrap">
        <a href="http://127.0.0.1:8800/docs" target="_blank" rel="noopener">API 文档</a>
      </footer>
    </div>
  `;

  bindEvents();
}

function bindEvents(): void {
  const form = document.querySelector<HTMLFormElement>("#entry-form");
  form?.addEventListener("submit", onSubmit);

  document.querySelectorAll<HTMLButtonElement>("[data-delete]").forEach((button) => {
    button.addEventListener("click", onDelete);
  });
}

async function loadData(): Promise<void> {
  state.loading = true;
  render();
  try {
    const [overview, entries] = await Promise.all([
      api.getOverview(),
      api.listEntries(),
    ]);
    state.overview = overview;
    state.entries = entries;
  } catch (error) {
    state.flash = {
      kind: "err",
      text: error instanceof Error ? error.message : "加载失败",
    };
  } finally {
    state.loading = false;
    render();
  }
}

async function onSubmit(event: Event): Promise<void> {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const data = new FormData(form);

  try {
    await api.createEntry({
      name: String(data.get("name") ?? "").trim(),
      dish: String(data.get("dish") ?? "").trim(),
      headcount: Number(data.get("headcount") ?? 1),
      note: String(data.get("note") ?? "").trim(),
    });
    form.reset();
    state.flash = { kind: "ok", text: "报名成功，期待见面～" };
    await loadData();
  } catch (error) {
    state.flash = {
      kind: "err",
      text: error instanceof ApiError ? error.message : "提交失败",
    };
    render();
  }
}

async function onDelete(event: Event): Promise<void> {
  const button = event.currentTarget as HTMLButtonElement;
  const entryId = button.dataset.delete;
  const name = button.dataset.name ?? "该用户";
  if (!entryId) return;

  if (!window.confirm(`确定取消 ${name} 的报名？`)) return;

  try {
    await api.deleteEntry(entryId);
    state.flash = { kind: "ok", text: "已取消报名" };
    await loadData();
  } catch (error) {
    state.flash = {
      kind: "err",
      text: error instanceof ApiError ? error.message : "取消失败",
    };
    render();
  }
}

void loadData();
