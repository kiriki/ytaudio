import mitt from 'mitt'

type Events = {
  ws_message: object;
  foo: string;
  bar?: number;
};
export const notifier = mitt<Events>()
