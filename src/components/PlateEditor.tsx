import React, { useMemo, useCallback } from 'react';
import { createEditor, Editor, Transforms, Element as SlateElement, Range } from 'slate';
import type { Descendant, BaseEditor } from 'slate';
import { Slate, Editable, withReact, ReactEditor } from 'slate-react';
import type { RenderElementProps, RenderLeafProps } from 'slate-react';
import { withHistory } from 'slate-history';
import './PlateEditor.css';

interface EnhancedEditorProps {
  value: Descendant[];
  onChange: (value: Descendant[]) => void;
}

// Custom types for our editor
type CustomEditor = BaseEditor & ReactEditor;

const LIST_TYPES = ['numbered-list', 'bulleted-list'];
const TEXT_ALIGN_TYPES = ['left', 'center', 'right', 'justify'];

const Element = ({ attributes, children, element }: RenderElementProps) => {
  const style: React.CSSProperties = { textAlign: (element as any).align };

  switch ((element as any).type) {
    case 'block-quote':
      return (
        <blockquote style={style} {...attributes}>
          {children}
        </blockquote>
      );
    case 'bulleted-list':
      return (
        <ul style={style} {...attributes}>
          {children}
        </ul>
      );
    case 'heading-one':
      return (
        <h1 style={style} {...attributes}>
          {children}
        </h1>
      );
    case 'heading-two':
      return (
        <h2 style={style} {...attributes}>
          {children}
        </h2>
      );
    case 'heading-three':
      return (
        <h3 style={style} {...attributes}>
          {children}
        </h3>
      );
    case 'list-item':
      return (
        <li style={style} {...attributes}>
          {children}
        </li>
      );
    case 'numbered-list':
      return (
        <ol style={style} {...attributes}>
          {children}
        </ol>
      );
    case 'link':
      return (
        <a
          {...attributes}
          href={(element as any).url}
          style={{ color: '#77ccdd', textDecoration: 'underline' }}
        >
          {children}
        </a>
      );
    case 'image':
      return (
        <div {...attributes}>
          <div contentEditable={false}>
            <img
              src={(element as any).url}
              alt={(element as any).alt || ''}
              style={{ maxWidth: '100%', height: 'auto', borderRadius: '4px' }}
            />
          </div>
          {children}
        </div>
      );
    case 'table':
      return (
        <table {...attributes} style={style}>
          <tbody>{children}</tbody>
        </table>
      );
    case 'table-row':
      return (
        <tr {...attributes} style={style}>
          {children}
        </tr>
      );
    case 'table-cell':
      return (
        <td {...attributes} style={style}>
          {children}
        </td>
      );
    default:
      return (
        <p style={style} {...attributes}>
          {children}
        </p>
      );
  }
};

const Leaf = ({ attributes, children, leaf }: RenderLeafProps) => {
  if ((leaf as any).bold) {
    children = <strong>{children}</strong>;
  }
  if ((leaf as any).code) {
    children = <code>{children}</code>;
  }
  if ((leaf as any).italic) {
    children = <em>{children}</em>;
  }
  if ((leaf as any).underline) {
    children = <u>{children}</u>;
  }
  if ((leaf as any).strikethrough) {
    children = <s>{children}</s>;
  }

  return <span {...attributes}>{children}</span>;
};

export const EnhancedEditor: React.FC<EnhancedEditorProps> = ({ value, onChange }) => {
  const editor = useMemo(() => withHistory(withReact(createEditor())), []);

  const renderElement = useCallback((props: RenderElementProps) => <Element {...props} />, []);
  const renderLeaf = useCallback((props: RenderLeafProps) => <Leaf {...props} />, []);

  const toggleMark = (format: string) => {
    const isActive = isMarkActive(editor, format);
    if (isActive) {
      Editor.removeMark(editor, format);
    } else {
      Editor.addMark(editor, format, true);
    }
  };

  const toggleBlock = (format: string) => {
    const isActive = isBlockActive(editor, format, TEXT_ALIGN_TYPES.includes(format) ? 'align' : 'type');
    const isList = LIST_TYPES.includes(format);

    Transforms.unwrapNodes(editor, {
      match: n =>
        !Editor.isEditor(n) &&
        SlateElement.isElement(n) &&
        LIST_TYPES.includes((n as any).type) &&
        !TEXT_ALIGN_TYPES.includes(format),
      split: true,
    });

    let newProperties: Partial<SlateElement>;
    if (TEXT_ALIGN_TYPES.includes(format)) {
      newProperties = {
        align: isActive ? undefined : format,
      } as any;
    } else {
      newProperties = {
        type: isActive ? 'paragraph' : isList ? 'list-item' : format,
      } as any;
    }

    Transforms.setNodes<SlateElement>(editor, newProperties);

    if (!isActive && isList) {
      const block = { type: format, children: [] };
      Transforms.wrapNodes(editor, block as any);
    }
  };

  const isBlockActive = (editor: CustomEditor, format: string, blockType: 'type' | 'align' = 'type') => {
    const { selection } = editor;
    if (!selection) return false;

    const [match] = Array.from(
      Editor.nodes(editor, {
        at: Editor.unhangRange(editor, selection),
        match: n =>
          !Editor.isEditor(n) && SlateElement.isElement(n) && (n as any)[blockType] === format,
      })
    );

    return !!match;
  };

  const isMarkActive = (editor: CustomEditor, format: string) => {
    const marks = Editor.marks(editor) as any;
    return marks ? marks[format] === true : false;
  };

  const insertLink = () => {
    const url = window.prompt('Sláðu inn vefslóð:');
    if (url && !isLinkActive(editor)) {
      wrapLink(editor, url);
    }
  };

  const isLinkActive = (editor: CustomEditor) => {
    const [link] = Editor.nodes(editor, {
      match: n => !Editor.isEditor(n) && SlateElement.isElement(n) && (n as any).type === 'link',
    });
    return !!link;
  };

  const unwrapLink = (editor: CustomEditor) => {
    Transforms.unwrapNodes(editor, {
      match: n => !Editor.isEditor(n) && SlateElement.isElement(n) && (n as any).type === 'link',
    });
  };

  const wrapLink = (editor: CustomEditor, url: string) => {
    if (isLinkActive(editor)) {
      unwrapLink(editor);
    }

    const { selection } = editor;
    const isCollapsed = selection && Range.isCollapsed(selection);
    const link: any = {
      type: 'link',
      url,
      children: isCollapsed ? [{ text: url }] : [],
    };

    if (isCollapsed) {
      Transforms.insertNodes(editor, link);
    } else {
      Transforms.wrapNodes(editor, link, { split: true });
      Transforms.collapse(editor, { edge: 'end' });
    }
  };

  const insertImage = () => {
    const url = window.prompt('Sláðu inn vefslóð myndar:');
    if (url) {
      const image: any = { type: 'image', url, children: [{ text: '' }] };
      Transforms.insertNodes(editor, image);
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const url = e.target?.result as string;
        const image: any = { type: 'image', url, children: [{ text: '' }] };
        Transforms.insertNodes(editor, image);
      };
      reader.readAsDataURL(file);
    }
    // Reset the input
    event.target.value = '';
  };

  const insertTable = () => {
    const rows = parseInt(window.prompt('Fjöldi raða:', '3') || '3');
    const cols = parseInt(window.prompt('Fjöldi dálka:', '3') || '3');
    
    if (rows > 0 && cols > 0 && rows <= 20 && cols <= 10) {
      const tableRows = Array.from({ length: rows }, () => ({
        type: 'table-row',
        children: Array.from({ length: cols }, () => ({
          type: 'table-cell',
          children: [{ text: '' }],
        })),
      }));

      const table: any = {
        type: 'table',
        children: tableRows,
      };

      Transforms.insertNodes(editor, table);
      // Insert a paragraph after the table
      Transforms.insertNodes(editor, {
        type: 'paragraph',
        children: [{ text: '' }],
      } as any);
    }
  };

  return (
    <div className="plate-editor-container">
      <Slate editor={editor} initialValue={value} onChange={onChange}>
        <div className="plate-toolbar">
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleMark('bold');
            }}
            className={isMarkActive(editor, 'bold') ? 'is-active' : ''}
            title="Feitletrað (Ctrl+B)"
          >
            <strong>B</strong>
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleMark('italic');
            }}
            className={isMarkActive(editor, 'italic') ? 'is-active' : ''}
            title="Skáletrað (Ctrl+I)"
          >
            <em>I</em>
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleMark('underline');
            }}
            className={isMarkActive(editor, 'underline') ? 'is-active' : ''}
            title="Undirstrikað (Ctrl+U)"
          >
            <u>U</u>
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleMark('strikethrough');
            }}
            className={isMarkActive(editor, 'strikethrough') ? 'is-active' : ''}
            title="Yfirstrikað"
          >
            <s>S</s>
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleMark('code');
            }}
            className={isMarkActive(editor, 'code') ? 'is-active' : ''}
            title="Kóði (Ctrl+`)"
          >
            {'</>'}
          </button>

          <div className="toolbar-separator" />

          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('heading-one');
            }}
            className={isBlockActive(editor, 'heading-one') ? 'is-active' : ''}
            title="Fyrirsögn 1"
          >
            H1
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('heading-two');
            }}
            className={isBlockActive(editor, 'heading-two') ? 'is-active' : ''}
            title="Fyrirsögn 2"
          >
            H2
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('heading-three');
            }}
            className={isBlockActive(editor, 'heading-three') ? 'is-active' : ''}
            title="Fyrirsögn 3"
          >
            H3
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('block-quote');
            }}
            className={isBlockActive(editor, 'block-quote') ? 'is-active' : ''}
            title="Tilvitnun"
          >
            " Tilvitnun
          </button>

          <div className="toolbar-separator" />

          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('numbered-list');
            }}
            className={isBlockActive(editor, 'numbered-list') ? 'is-active' : ''}
            title="Númeraður listi"
          >
            1. Listi
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              toggleBlock('bulleted-list');
            }}
            className={isBlockActive(editor, 'bulleted-list') ? 'is-active' : ''}
            title="Punktalisti"
          >
            • Listi
          </button>

          <div className="toolbar-separator" />

          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              insertLink();
            }}
            title="Setja inn tengil"
          >
            🔗 Tengill
          </button>
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              insertImage();
            }}
            title="Setja inn mynd frá vefslóð"
          >
            🖼️ Vefslóð
          </button>
          <button
            type="button"
            onClick={() => {
              document.getElementById('image-upload')?.click();
            }}
            title="Hlaða upp mynd"
          >
            📤 Hlaða upp
          </button>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            style={{ display: 'none' }}
          />
          
          <div className="toolbar-separator" />
          
          <button
            type="button"
            onMouseDown={(e) => {
              e.preventDefault();
              insertTable();
            }}
            title="Setja inn töflu"
          >
            📊 Tafla
          </button>
        </div>
        <Editable
          className="plate-content"
          renderElement={renderElement}
          renderLeaf={renderLeaf}
          placeholder="Skrifaðu efni fréttarinnar hér..."
          spellCheck
          autoFocus
        />
      </Slate>
    </div>
  );
};
