defmodule Consistency do
  @moduledoc false
  def myfun( p1 , p2 ) when is_list(p2) do
      if p1 == p2 do
      p1
      else
      p2 + p1
    end
  end
end
