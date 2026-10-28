/** Sentimeter integration profile v1; AG-UI wire types are provided by @ag-ui/core. */
export type TranscriptSegment = {
  id: string; callId: string; speaker: 'customer' | 'operator';
  text: string; revision: number; isFinal: boolean;
  startMs: number; endMs: number;
};
export type AgentActivity = {
  id: string; name: string; task: string;
  status: 'waiting' | 'running' | 'completed' | 'error';
};
export type Evidence = {
  screen: string; reference: string; fields: [string, string][];
  columns: string[]; rows: string[][]; conclusion: string; note?: string;
};
export type EvidenceCard = {
  id: 't24' | 'fimi' | 'policy' | 'mcc' | 'ido' | 'portal' | `route-${1|2|3|4}-${0|1|2|3}`;
  source: string; title: string; status: string; body: string;
  evidence: Evidence; warn?: boolean;
};
export type AgentState = {
  cards: EvidenceCard[]; agents: AgentActivity[];
  recommendation: null | { title: string; answer: string; solution: string };
  signals: { emotion: string; confidence: string; guidance: string };
};
export type OperatorAction = {
  id: string; callId: string; mode: 'demo' | 'live'; timestamp: number;
  type: 'accept_call' | 'confirm_identity_field' | 'select_classification' |
        'hold_call' | 'end_call' | 'resume_call' | 'create_followup_case' | 'call_complete';
  payload: Record<string, unknown>;
};
export type EventScope = { callId?: string; runId?: string; epoch?: number };
export interface SentimeterInterface {
  version: '1.0.0'; callId: string;
  setMode(mode: 'demo' | 'live'): void;
  ingestTranscript(segment: TranscriptSegment): boolean;
  receiveEvent(event: import('@ag-ui/core').BaseEvent, scope?: EventScope): boolean;
  getRunInput(): import('@ag-ui/core').RunAgentInput;
  getState(): AgentState;
  getTranscript(): TranscriptSegment[];
  getEvents(): unknown[];
  connectAgent(options: {url: string; input?: import('@ag-ui/core').RunAgentInput; headers?: Record<string,string>}): Promise<void>;
  disconnect(): void;
  setCallState(state: {callId: string; verified?: {dob:boolean;id:boolean}; eligible?: {dob:boolean;id:boolean}; followupAllowed?:boolean; phase?: 'live'|'ringing'|'awaiting-hold'|'answer-ready'|'followup'|'complete'; elapsedSeconds?:number; classification?:(string|null|boolean)[]; followupConfirmed?:boolean}): boolean;
}
