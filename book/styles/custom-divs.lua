-- Pandoc Lua Filter: Convert custom fenced divs to styled output
-- Handles: .infobox, .szene

function Div(el)
  -- Infobox
  if el.classes:includes("infobox") then
    if FORMAT:match("latex") then
      -- Extract title from first header if present
      local title = ""
      local content = el.content
      if #content > 0 and content[1].t == "Header" then
        title = pandoc.utils.stringify(content[1])
        table.remove(content, 1)
      end
      local open = pandoc.RawBlock("latex", "\\begin{infobox}[" .. title .. "]")
      local close = pandoc.RawBlock("latex", "\\end{infobox}")
      table.insert(content, 1, open)
      table.insert(content, close)
      return content
    elseif FORMAT:match("html") or FORMAT:match("epub") then
      -- HTML/EPUB: just add class, CSS handles styling
      return el
    end
  end

  -- Szene (scene/vision)
  if el.classes:includes("szene") then
    if FORMAT:match("latex") then
      local content = el.content
      local open = pandoc.RawBlock("latex", "\\begin{szene}")
      local close = pandoc.RawBlock("latex", "\\end{szene}")
      table.insert(content, 1, open)
      table.insert(content, close)
      return content
    elseif FORMAT:match("html") or FORMAT:match("epub") then
      return el
    end
  end
end
